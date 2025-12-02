import argparse
import datetime
import pathlib
import textwrap
import tomllib


def load_agent():
    with open("VideoMachine-Agent.toml", "rb") as f:
        data = tomllib.load(f)
    agent = data.get("agent", {})
    return (
        agent.get("name", "VideoMachine"),
        agent.get("description", "").strip(),
        agent.get("instructions", "").strip(),
    )


def format_prompt(topic: str) -> str:
    agent_name, description, instructions = load_agent()
    task = textwrap.dedent(
        f"""\
        產出完整 60 秒短視頻製作包，主題：{topic}
        - 60 秒腳本（反敘事開頭、刺痛現實、高維解釋、例子、可執行方案、金句、CTA）
        - 14 鏡頭分鏡：畫面描述 / 旁白 / AI Prompt（每鏡頭）
        - BGM 建議（LoFi/Ambient/Synthwave/Minimal Piano，80-95 BPM，清醒克制）
        - 標題若干
        - Thumbnail Prompt（深色、留白、極簡城市夜景、清醒哲學感）
        - 收尾金句與 CTA
        """
    )
    header = textwrap.dedent(
        f"""\
        Agent: {agent_name}
        Description: {description}
        Mode: auto
        Topic: {topic}
        Task: {task}
        Output 要求：繁體中文、卡卡語氣，避免模板化與雞湯。
        """
    )
    return f"{header}\n{instructions}\n"


def main():
    parser = argparse.ArgumentParser(description="Generate prompt for VideoMachine agent.")
    parser.add_argument("--topic", required=True, help="影片主題")
    parser.add_argument("--run-id", help="輸出子目錄名，預設時間戳")
    parser.add_argument(
        "--output-base",
        default="03-outputs/videomachine-agent",
        help="輸出根目錄，預設 03-outputs/videomachine-agent",
    )
    args = parser.parse_args()

    run_id = args.run_id or datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = pathlib.Path(args.output_base) / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    prompt_text = format_prompt(args.topic)
    output_file = output_dir / "prompt.txt"
    output_file.write_text(prompt_text, encoding="utf-8")
    print(f"Wrote prompt to {output_file.resolve()}")


if __name__ == "__main__":
    main()
