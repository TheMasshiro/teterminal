from abc import ABC, abstractmethod
from typing import Any

from flask import render_template


class MainInterface(ABC):
    @abstractmethod
    def index(self) -> Any:
        pass

    @abstractmethod
    def dashboard_admin(self) -> Any:
        pass

    @abstractmethod
    def dashboard_client(self) -> Any:
        pass


class Main:
    def index(self):
        return render_template("index.html", title="Home")

    def dashboard_admin(self):
        return render_template("main/dashboard.html", title="Dashboard", is_admin=True)

    def dashboard_client(self):
        return render_template("main/dashboard.html", title="Dashboard", is_admin=False)
