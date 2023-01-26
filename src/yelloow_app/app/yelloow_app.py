from yelloow_models.models import KPIName
from yelloow_adapters import XLSXAdapter
def run_yelloow_app():
    k = KPIName(
        dutch="test",
        german="test",
        english="test",
        french="test",
    )
    x = XLSXAdapter()
    
    print(k)


if __name__ == "__main__":
    run_yelloow_app()
