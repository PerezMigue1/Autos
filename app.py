import os
from io import BytesIO, StringIO

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from flask import Flask, Response, render_template, request, send_file
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder


app = Flask(__name__)

DATA_PATH = "processes2.csv"
MODEL_PATH = "model/modelo_autos.pkl"
TARGET = "selling_price"
FEATURES = [
    "max_power (in bph)",
    "year",
    "Engine (CC)",
    "km_driven",
    "Mileage",
    "name",
]

LABELS = {
    "name": "Marca",
    "year": "Ano del vehiculo",
    "km_driven": "Kilometraje",
    "max_power (in bph)": "Potencia maxima (bhp)",
    "Mileage": "Rendimiento",
    "Engine (CC)": "Motor (CC)",
}


def save_model_charts(y_test, predictions, metrics):
    charts_dir = os.path.join(app.static_folder, "charts")
    os.makedirs(charts_dir, exist_ok=True)

    scatter_path = os.path.join(charts_dir, "reales_vs_predicciones.png")
    residuals_path = os.path.join(charts_dir, "distribucion_residuos.png")

    plt.figure(figsize=(8, 6))
    plt.scatter(
        y_test,
        predictions,
        alpha=0.5,
        color="steelblue",
        edgecolors="white",
        linewidths=0.3,
    )
    limits = [
        min(y_test.min(), predictions.min()),
        max(y_test.max(), predictions.max()),
    ]
    plt.plot(limits, limits, "r--", linewidth=1.5, label="Prediccion perfecta")
    plt.xlabel("Valores reales (selling_price)")
    plt.ylabel("Predicciones")
    plt.title(
        f"Valores reales vs predicciones\n"
        f"R2 = {metrics['r2_split']:.4f} | MAE = {metrics['mae_split']:.2f}"
    )
    plt.legend()
    plt.tight_layout()
    plt.savefig(scatter_path, dpi=150)
    plt.close()

    residuals = y_test - predictions
    plt.figure(figsize=(9, 5))
    sns.histplot(residuals, kde=True, color="steelblue", bins=40)
    plt.axvline(0, color="red", linestyle="--", linewidth=1.5, label="Residuo = 0")
    plt.axvline(
        residuals.mean(),
        color="orange",
        linestyle="--",
        linewidth=1.5,
        label=f"Media = {residuals.mean():,.0f}",
    )
    plt.title("Distribucion de los residuos")
    plt.xlabel("Residuos (real - predicho)")
    plt.ylabel("Frecuencia")
    plt.legend()
    plt.tight_layout()
    plt.savefig(residuals_path, dpi=150)
    plt.close()

    return {
        "scatter": "charts/reales_vs_predicciones.png",
        "residuals": "charts/distribucion_residuos.png",
    }


def build_model():
    df = pd.read_csv(DATA_PATH, index_col=0)
    numeric_cols = df.select_dtypes(include="number").columns
    text_cols = df.select_dtypes(include="object").columns

    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    df[text_cols] = df[text_cols].fillna(df[text_cols].mode().iloc[0])

    x = df[FEATURES]
    y = df[TARGET]

    categorical_features = ["name"]
    numeric_features = [column for column in FEATURES if column not in categorical_features]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
                categorical_features,
            ),
            ("numeric", "passthrough", numeric_features),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(n_estimators=100, random_state=42)),
        ]
    )

    scores_r2 = cross_val_score(model, x, y, cv=7, scoring="r2")
    scores_mae = -cross_val_score(model, x, y, cv=7, scoring="neg_mean_absolute_error")

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    metrics = {
        "r2_cv": float(scores_r2.mean()),
        "mae_cv": float(scores_mae.mean()),
        "r2_split": float(r2_score(y_test, predictions)),
        "mae_split": float(mean_absolute_error(y_test, predictions)),
    }
    charts = save_model_charts(y_test, predictions, metrics)

    model.fit(x, y)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    dump(model, MODEL_PATH)
    return df, model, metrics, charts


DF, MODEL, METRICS, CHARTS = build_model()
BRANDS = sorted(DF["name"].dropna().unique().tolist())


def results_dataframe():
    return pd.DataFrame(
        [
            {"Metrica": "R2 promedio CV=7", "Valor": round(METRICS["r2_cv"], 6)},
            {"Metrica": "MAE promedio CV=7", "Valor": round(METRICS["mae_cv"], 2)},
            {"Metrica": "R2 corrida independiente", "Valor": round(METRICS["r2_split"], 6)},
            {"Metrica": "MAE corrida independiente", "Valor": round(METRICS["mae_split"], 2)},
        ]
    )


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    form_values = {
        "name": BRANDS[0],
        "year": 2017,
        "km_driven": 45000,
        "max_power": 81.86,
        "mileage": 20.14,
        "engine": 1197,
    }

    if request.method == "POST":
        form_values = {
            "name": request.form.get("name", BRANDS[0]),
            "year": request.form.get("year", ""),
            "km_driven": request.form.get("km_driven", ""),
            "max_power": request.form.get("max_power", ""),
            "mileage": request.form.get("mileage", ""),
            "engine": request.form.get("engine", ""),
        }

        input_data = pd.DataFrame(
            [
                {
                    "name": form_values["name"],
                    "year": float(form_values["year"]),
                    "km_driven": float(form_values["km_driven"]),
                    "max_power (in bph)": float(form_values["max_power"]),
                    "Mileage": float(form_values["mileage"]),
                    "Engine (CC)": float(form_values["engine"]),
                }
            ]
        )[FEATURES]
        prediction = float(MODEL.predict(input_data)[0])

    return render_template(
        "index.html",
        brands=BRANDS,
        labels=LABELS,
        metrics=METRICS,
        charts=CHARTS,
        prediction=prediction,
        form_values=form_values,
    )


@app.route("/download/csv")
def download_csv():
    buffer = StringIO()
    results_dataframe().to_csv(buffer, index=False)
    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=resultados_modelo.csv"},
    )


@app.route("/download/excel")
def download_excel():
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        results_dataframe().to_excel(writer, sheet_name="Metricas", index=False)
        DF[FEATURES + [TARGET]].head(100).to_excel(
            writer, sheet_name="Muestra dataset", index=False
        )
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="resultados_modelo.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


if __name__ == "__main__":
    app.run(debug=True, port=5055)
