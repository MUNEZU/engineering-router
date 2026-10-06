# 🐈 Engineering Router

为 Codex 软件工程任务提供明确的分工、模型路由和独立审查规则。

Engineering Router 把一个主线程与六种专职角色组合成小队：主线程负责决策和交付，子 agent 只处理边界清晰的调查、实现、咨询或审查。简单任务可以不委派；复杂任务按风险选择角色，不以“开更多 agent”为目标。

这是一个 **Codex Skill + 自定义 agent 配置**，不是独立调度服务，也不需要 AI Control Plane。当前版本为 **2.2.0**；版本变化见 [CHANGELOG](CHANGELOG.md)。

从这里开始：[安装](#安装) → [首次使用](#使用) → [确认路由](#诊断与用量)。

> 当前存在运行时权限限制：配置为只读的子 agent 可能继承主线程的写权限。使用前请阅读[权限与适用边界](#权限与适用边界)；本项目不提供独立的沙箱隔离保证。

## 目录

- [安装](#安装)
- [使用](#使用)
- [分工与模型](#分工与模型)
- [诊断与用量](#诊断与用量)
- [权限与适用边界](#权限与适用边界)
- [更新与回退](#更新与回退)
- [开发与贡献](#开发与贡献)
- [来源与许可](#来源与许可)

## 安装

### 前置条件

- Codex 客户端支持自定义 agent 和多 agent 调度，并能应用所需的模型、推理强度和权限配置。
- 账号能够使用角色表中的模型。模型不可用时，路由应报告并停止，不自动换用其他模型。
- Git 用于获取源码；诊断脚本和测试使用 Python **3.11 或更新版本**，不需要额外 Python 依赖。

以下为 macOS / Linux 的手动安装方式。先结束或停止正在运行的 Codex 任务及其子 agent，避免同一次任务混用新旧配置。

```bash
git clone https://github.com/MUNEZU/engineering-router.git
cd engineering-router
python3 -m unittest discover -s tests -v
```

确认测试通过后，备份同名配置并安装。本段只写入 `engineering-router` Skill 和本仓库的六个 agent 文件，不修改 `config.toml`、全局 `AGENTS.md` 或其他 agent。

```bash
(
  set -eu
  router_codex_dir="${CODEX_HOME:-$HOME/.codex}"
  mkdir -p "$router_codex_dir"
  router_backup_dir="$(mktemp -d "$router_codex_dir/engineering-router-backup.XXXXXX")"
  mkdir -p "$router_backup_dir/agents"
  if [ -d "$router_codex_dir/skills/engineering-router" ]; then
    cp -R "$router_codex_dir/skills/engineering-router" "$router_backup_dir/skill"
  fi
  for profile in agents/*.toml; do
    profile_name="$(basename "$profile")"
    if [ -e "$router_codex_dir/agents/$profile_name" ]; then
      cp -p "$router_codex_dir/agents/$profile_name" "$router_backup_dir/agents/"
    fi
  done
  mkdir -p "$router_codex_dir/skills/engineering-router" "$router_codex_dir/agents"
  cp -R skills/engineering-router/. "$router_codex_dir/skills/engineering-router/"
  cp agents/*.toml "$router_codex_dir/agents/"
  printf 'Backup: %s\n' "$router_backup_dir"
)
```

保存输出的备份路径。安装后重启 Codex 或打开新 chat，让客户端重新发现 Skill 和角色配置；安装完成不等于运行时验证通过。

主线程模型仍由你在客户端设置，推荐 `gpt-6.1-sol` / `medium`。公开包不包含机器专用的 `local-overlay/`，也不会自动修改个人工作协议。

## 使用

在新的 Codex chat 中明确调用 Skill，并描述目标、范围和验收条件。例如：

```text
$engineering-router
检查登录失败的原因。先只读调查，给出证据和影响范围，不修改代码。
```

```text
$engineering-router
修复这个模块的重复提交问题。保持现有 API 不变，补回归测试；
如果涉及并发或数据一致性，按高风险路径实现并做独立审查。
```

每一轮首次激活时，Skill 会输出一次：

```text
🐈 已开启小队模式。
```

英语对应 `🐈 Team Mode activated.`；同一轮的路由调整不会重复输出。激活提示说明 Skill 已被加载，不证明子 agent 已启动或模型、权限已正确生效。

你可以明确要求“不使用子 agent”、指定模型或限制修改范围。这些要求以及项目规则优先于默认路由；用户授权范围不会因委派而扩大。

常用流程还包括[代码库探索](skills/engineering-router/references/explore.md)、[稳定变更后的简化](skills/engineering-router/references/simplify.md)和[交互测试](skills/engineering-router/references/interactive-testing.md)。它们是按需使用的工作规则，不是每个任务都必须执行的流水线。

## 分工与模型

主线程负责拆解、未决问题、权限、整合与最终验收。子 agent 接收明确的目标、非目标、允许范围和检查要求，而不是重新规划整个项目。

| 角色 | 默认模型 | 推理强度 | 配置权限¹ | 适用工作 |
| --- | --- | --- | --- | --- |
| `code_explorer` | `gpt-5.6-luna` | medium | read-only | 入口、调用链、根因和影响范围调查 |
| `code_writer` | `gpt-5.6-luna` | medium | workspace-write | 清晰、局部、低风险修改 |
| `luna_worker` | `gpt-5.6-luna` | max | workspace-write | 不跨受保护边界的较深实现 |
| `hard_code_writer` | `gpt-6.1-sol` | high | workspace-write | 高风险、跨模块、架构或契约敏感实现 |
| `independent_reviewer` | `gpt-6.1-sol` | high | read-only | 新上下文中的独立审查 |
| `expert_advisor` | 调度时明确指定 | 调度时明确指定 | read-only | 需要独立判断的复杂咨询 |

¹ 这是文件中的预期配置，不是运行时权限保证，见[权限与适用边界](#权限与适用边界)。

`expert_advisor` 不固定模型和推理强度：通常请求 `gpt-6.1-sol` / `high`；额外用量得到明确授权后，才使用 `max`。`gpt-6-astra` 通常以 `medium` 用于关键咨询或单独审查，但必须由用户或有效交接明确选择，不能因任务重要就自动启用。

默认路由遵循以下规则：

- 简单工作可使用零个子 agent；一个有界问题默认一个子 agent。自主并发通常最多两个，必要的设计或独立审查覆盖可以例外。
- 新子 agent 不继承历史对话；只在原任务的直接续作中复用。独立审查始终使用新 reviewer。
- 子 agent 被要求不创建后代、不彼此直接通信；并行写入必须分配互不重叠的文件或范围。这些是工作协议，不是额外的系统级隔离机制。
- 涉及授权、安全、迁移、支付、数据完整性、不可逆操作或公开契约的实现，不交给 `luna_worker`，应走高风险实现与独立审查路径。
- 不默认使用 `gpt-6-sol` 或 `gpt-6-luna`，不因失败或额度压力静默更换模型。外部厂商必须被明确选择；本包不提供外部 CLI 执行器。

完整契约见 [Skill](skills/engineering-router/SKILL.md) 和[角色与路由说明](skills/engineering-router/references/profiles-routing.md)。

## 诊断与用量

在仓库根目录执行：

```bash
# 尽力识别当前主线程的实际模型
python3 skills/engineering-router/scripts/current_model.py

# 按模型、角色和会话汇总本地保留用量
python3 skills/engineering-router/scripts/usage_by_model.py --all --by-agent --by-session

# 汇总指定主任务及其子 agent，输出 JSON
python3 skills/engineering-router/scripts/usage_by_model.py --task-id YOUR_THREAD_ID --by-agent --by-session --json
```

将 `YOUR_THREAD_ID` 替换为实际任务 ID。在设置了 `CODEX_THREAD_ID` 的 Codex 执行环境中，也可以使用 `--task-id current`；普通终端未必具备这个变量。

脚本默认读取本地活动会话；归档仅通过 `--archived-sessions-root <path>` 明确纳入。`--days 7` 筛选的是最近七个本地自然日**创建的会话**并汇总其保留用量，不是严格按事件时间统计的“最近一周账单”。

结果是本地 token 观测和带日期的 Standard credits 估算。缺失、临时或未保留的记录可能使结果不完整；它不能据此精确换算 Plus 额度，也不能证明混合服务档位的实际计费。账号额度、重置时间和剩余用量以产品的账号用量视图为准。

判断是否正常工作时，不只看激活提示：还应从实际 trace 核对角色、模型、推理强度、有效权限、父子关系和层级，并检查产出与验收结果。详见[评估指南](skills/engineering-router/references/evaluation.md)。

## 权限与适用边界

**已知限制：只读配置可能被父线程的运行时权限覆盖。** 2026-10-04 的桌面实测在新 chat 中也观察到了这一行为。当前模型更新没有修复它；如果有效权限与角色要求不一致，应停止该路由并报告，不能把提示词中的“只读”视作强制隔离。

自定义角色可用性、模型访问和配置应用取决于客户端。TOML 文件、spawn 请求或子 agent 自述都不是执行证据；无法确认精确组合时，不应声称路由已经通过验证。

本包不安装 `default.toml` 哨兵，不主动请求 Fast 服务档位，也不保证父线程的运行时覆盖不会影响实际服务档位。并行与低成本角色旨在限制不必要的委派，**不保证节省固定比例的额度**。

诊断脚本不上传数据，但输出可能包含任务 ID、路径、角色和用量元数据。提交 issue 前请脱敏；不要公开原始 trace、提示词、凭据、私有源码或个人数据。

## 更新与回退

更新前结束活动任务，在可信 checkout 中获取新版本，再执行安装段的测试、备份和复制步骤。只替换本 Skill 和六个同名角色文件；不要覆盖其他 agent 或个人规则。跨版本变化先查阅 [CHANGELOG](CHANGELOG.md)。

回退时，从保存的备份恢复原 Skill 目录和同名角色文件；只移除失败安装新增、且备份中原本不存在的本包文件。不要批量清理 `agents/` 或恢复整个 Codex 配置目录。

更新或回退后都需要重新加载配置，并通过一个有界任务核对实际路由。静态测试通过不代表客户端权限隔离已生效。

## 开发与贡献

仓库中的 `skills/engineering-router/` 是 Skill 与按需参考资料，`agents/` 是六种角色配置，`tests/` 覆盖路由契约、配置和诊断脚本。使用以下命令运行测试：

```bash
python3 -m unittest discover -s tests -v
```

公开 checkout 不含机器专用 overlay，相应的本地测试会跳过。这不影响公开包测试，但也不能替代真实客户端中的路由验证。

欢迎通过 [Issues](https://github.com/MUNEZU/engineering-router/issues) 反馈问题，或提交 PR。报告路由问题时，请提供客户端版本、预期与实际角色/模型/权限以及脱敏后的最小复现；修改角色或规则时，请同步更新文档和测试。维护者：[MUNEZU](https://github.com/MUNEZU)。

## 来源与许可

本项目基于 [oil-oil/codex-team-mode](https://github.com/oil-oil/codex-team-mode) 的架构、工作流程和部分诊断内容进行适配，保留上游署名；不是官方 Codex 产品，也不声称与上游完全兼容。

以 [MIT License](LICENSE) 发布。上游版权声明与适配说明见 [NOTICE.md](NOTICE.md)。
