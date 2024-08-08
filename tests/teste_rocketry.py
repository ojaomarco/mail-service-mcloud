from rocketry import Rocketry
from datetime import datetime


app = Rocketry()


@app.task("every 5 seconds")
def do_things():
    # print("teste", datetime.weekday())

    agora = datetime.now()
    data_e_hora_formatadas = agora.strftime("%Y-%m-%d %H:%M:%S")
    print("Data e hora atuais:", data_e_hora_formatadas)


if __name__ == "__main__":
    app.run()
