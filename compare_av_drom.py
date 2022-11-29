import pandas as pd
from openpyxl.reader.excel import load_workbook


def compare():
    df_by = pd.read_excel('cars.xlsx', sheet_name='by')
    df_ru = pd.read_excel('cars.xlsx', sheet_name='ru', dtype={i: j for i, j in df_by.dtypes.items()})

    agg_func_math = {
        'price_usd': ['min', 'max', 'median', 'count']
    }
    # pd.options.display.max_columns = None
    # pd.options.display.max_seq_items = None
    # pd.set_option('display.width', 320)
    # pd.set_option('display.max_columns', 20)
    df_by = df_by.groupby(['brand', 'model', 'year', 'transmission', 'volume', 'engine']) \
        .agg(agg_func_math) \
        .round(2).reset_index()
    df_ru = df_ru.groupby(['brand', 'model', 'year', 'transmission', 'volume', 'engine']) \
        .agg(agg_func_math) \
        .round(2).reset_index()

    df = pd.merge(left=df_by, right=df_ru, on=['brand', 'model', 'year', 'transmission', 'volume', 'engine'],
                  how='outer',
                  suffixes=('_av_by', '_drom_ru'))
    with pd.ExcelWriter('cars.xlsx', engine="openpyxl", mode='a') as writer:
        workBook = writer.book
        try:
            workBook.remove(workBook['Compare'])
        except:
            print("worksheet doesn't exist")
        finally:
            df.to_excel(writer, sheet_name='Compare')


if __name__ == '__main__':
    compare()
