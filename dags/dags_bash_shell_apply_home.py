import dateutil.utils
from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id="dags_bash_shell_apply_home",
    schedule="0 18 * * *",
    start_date=pendulum.datetime(2024, 5, 1, tz="Asia/Seoul"),
    catchup=False
) as dag:
    task_01 = BashOperator(
        task_id="task_01",
        bash_command="/nas/dpfm/test/apply_home_api.sh {}".format(dateutil.utils.today().strftime("%Y%m%d"))
    )

    task_01


