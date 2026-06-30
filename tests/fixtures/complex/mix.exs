defmodule ComplexFixture.MixProject do
  use Mix.Project

  def project do
    [
      app: :complex_fixture,
      version: "0.1.0",
      deps: deps()
    ]
  end

  defp deps do
    [
      {:phoenix, "1.7.10"},
      {:ecto_sql, "3.11.0"},
      {:jason, "1.4", only: :dev},
      {:credo, "1.7.0", only: :dev, runtime: false}
    ]
  end
end
