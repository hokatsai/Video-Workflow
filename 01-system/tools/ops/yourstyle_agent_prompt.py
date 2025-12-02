import argparse
import datetime
import pathlib
import textwrap
import tomllib


def load_agent():
    with open("YourStyle-Agent.toml", "rb") as f:
        data = tomllib.load(f)
    agent = data.get("agent", {})
    return (
        agent.get("name", "YourStyle"),
        agent.get("description", "").strip(),
        agent.get("instructions", "").strip(),
    )


def build_task(mode: str, topic: str | None, count: int) -> str:
    topic_text = topic or "（未指定主題，可自行選擇核心話題）"
    if mode == "video":
        return f"產出 60 秒短視頻腳本，聚焦主題：{topic_text}。遵循 0-3s 反敘事、3-12s 刺痛現實、12-25s 高維解釋、25-38s 生活例子、38-50s 可執行方案、50-56s 金句、56-60s CTA 的節奏。"
    if mode == "long":
        return f"產出 3-5 分鐘深度腳本，聚焦主題：{topic_text}，保持反敘事開場、務實行動指南與金句收尾。"
    if mode == "title":
        return f"為主題「{topic_text}」生成 10 個爆款標題（短、反敘事、有穿透力）。"
    if mode == "matrix":
        return "生成 30 天內容矩陣（每天一個切題方向，涵蓋 8 大內容領域，可交叉組合）。"
    if mode == "quote":
        return f"針對主題「{topic_text}」給出 1-3 句金句（冷靜有力，避免雞湯）。"
    if mode == "ideas":
        return f"提供 {count} 條內容方向點子，面向主題「{topic_text}」，每條 1 句概念。"
    if mode == "persona":
        return "輸出卡卡式人設強化文案，總結語氣與角色設定，方便後續連貫創作。"
    return f"聚焦主題「{topic_text}」生成內容。"


def format_prompt(mode: str, topic: str | None, count: int) -> str:
    agent_name, description, instructions = load_agent()
    task = build_task(mode, topic, count)
    header = textwrap.dedent(
        f"""\
        Agent: {agent_name}
        Description: {description}
        Mode: {mode}
        Topic: {topic or "（未指定）"}
        Task: {task}
        """
    )
    output_rules = textwrap.dedent(
        """\
        Output 格式要求：
        - 以繁體中文輸出。
        - 不得輸出雞湯/模板話術。
        - 嚴格保持卡卡語氣（冷靜、反敘事、可執行、有力量）。
        """
    )
    return f"{header}\n{output_rules}\n\n{instructions}\n"


def main():
    parser = argparse.ArgumentParser(description="Generate prompt for YourStyle agent.")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["video", "long", "title", "matrix", "quote", "ideas", "persona"],
        help="選擇任務模式",
    )
    parser.add_argument("--topic", help="內容主題（部分模式可留空）")
    parser.add_argument(
        "--count", type=int, default=10, help="ideas 模式的點子數量（預設 10）"
    )
    parser.add_argument("--run-id", help="輸出子目錄名，預設時間戳")
    parser.add_argument(
        "--output-base",
        default="03-outputs/yourstyle-agent",
        help="輸出根目錄，預設 03-outputs/yourstyle-agent",
    )
    args = parser.parse_args()

    run_id = args.run_id or datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = pathlib.Path(args.output_base) / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    prompt_text = format_prompt(args.mode, args.topic, args.count)
    output_file = output_dir / "prompt.txt"
    output_file.write_text(prompt_text, encoding="utf-8")
    print(f"Wrote prompt to {output_file.resolve()}")


if __name__ == "__main__":
    main()
