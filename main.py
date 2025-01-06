import schedule
import time
from arxiv_bot.agent import ArxivPaperAgent

def main():
    agent = ArxivPaperAgent()
    # agent.run()  # 取消注释以立即运行一次
    
    schedule_times = agent.config.get_general_config()['schedule_time']
    if isinstance(schedule_times, str):
        schedule_times = [schedule_times]
    
    for schedule_time in schedule_times:
        schedule.every().day.at(schedule_time).do(agent.run)
        print(f"已设置定时任务：每天 {schedule_time} 运行")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 