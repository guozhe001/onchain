from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore

from evm_chain.handler import uniswap_handler

# 实例化调度器
scheduler = BackgroundScheduler()
# 调度器使用默认的DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), 'default')


def get_crontrigger(dt: datetime):
    return CronTrigger(second=dt.second, minute=dt.minute, hour=dt.hour, day=dt.day, month=dt.month, year=dt.year)


# 监听uni swap的新pair, 在程序启动一分钟之后开始
scheduler.add_job(uniswap_handler.listen_uni_pair_created, id='listen_uni_pair_created',
                  trigger=get_crontrigger(datetime.now() + timedelta(minutes=1)), max_instances=1,
                  replace_existing=True)

# 监听pancake swap的新pair, 在程序启动一分钟之后开始
scheduler.add_job(uniswap_handler.listen_pancake_pair_created, id='listen_pancake_pair_created',
                  trigger=get_crontrigger(datetime.now() + timedelta(minutes=1)), max_instances=1,
                  replace_existing=True)


def start():
    print("hello schedule")
    scheduler.start()
