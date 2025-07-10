# main.py
import typer

app = typer.Typer()


@app.command()
def agent(query: str):
    typer.echo(f"query: {query}")


if __name__ == "__main__":
    app()
