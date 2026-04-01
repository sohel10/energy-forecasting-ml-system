import psycopg2


def save_predictions(test, forecast, conf_int):

    conn = psycopg2.connect(
        host="localhost",
        database="weather_db",
        user="postgres",
        password="1234"
    )

    cursor = conn.cursor()

    # 🔥 Updated table (with confidence interval)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        datetime TIMESTAMP,
        actual FLOAT,
        predicted FLOAT,
        lower_ci FLOAT,
        upper_ci FLOAT
    )
    """)

    results = []

    for i in range(len(forecast)):

        dt = test.index[i]
        actual = float(test['energy_output'].iloc[i])
        pred = float(forecast.iloc[i])

        lower = float(conf_int.iloc[i, 0])
        upper = float(conf_int.iloc[i, 1])

        # 🔥 Insert into DB
        cursor.execute("""
        INSERT INTO predictions (datetime, actual, predicted, lower_ci, upper_ci)
        VALUES (%s, %s, %s, %s, %s)
        """, (dt, actual, pred, lower, upper))

        # 🔥 Return to API
        results.append({
            "datetime": str(dt),
            "actual": actual,
            "predicted": pred,
            "lower": lower,
            "upper": upper
        })

    conn.commit()
    conn.close()

    return results