import struct
import csv
from typing import Dict, Any


class BurmaldaDBEngine:
    """
    Движок СУБД «Бурмалда» для чтения .bin файлов (согласно спецификации типов)
    и красивого парсинга CSV-файлов.
    """

    @staticmethod
    def read_bin_file(file_path: str) -> Dict[str, Any]:
        """
        Чтение бинарного файла СУБД с учетом типов:
        - int (4 bytes) -> ID записи
        - smallint (2 bytes) -> Статус / Код ячейки рулетки
        - float (4 bytes) -> Значение (Score / Balance)
        - char(50) (50 bytes) -> Текстовое поле / Имя
        """
        records = []
        try:
            with open(file_path, 'rb') as f:
                # Читаем сигнатуру (например, 4 байта 'BMDB')
                header = f.read(4)
                if header != b'BMDB':
                    return {"status": "error", "message": "Неверный формат сигнатуры .bin (ожидается BMDB)"}

                # Количество записей (int - 4 байта)
                count_bytes = f.read(4)
                if not count_bytes:
                    return {"status": "success", "headers": ["ID", "Code", "Score", "Name"], "records": []}

                count = struct.unpack('<I', count_bytes)[0]

                # Размер одной записи согласно типам:
                # int (4) + smallint (2) + float (4) + char(50) (50) = 60 байт
                record_format = '<I h f 50s'
                record_size = struct.calcsize(record_format)

                for _ in range(count):
                    data = f.read(record_size)
                    if len(data) < record_size:
                        break

                    record_id, code, score, name_bytes = struct.unpack(record_format, data)

                    # Декодируем char(50), убирая нулевые байты
                    name = name_bytes.decode('utf-8', errors='ignore').rstrip('\x00')

                    records.append({
                        "id": record_id,
                        "code": code,
                        "score": round(score, 2),
                        "name": name
                    })

            return {
                "status": "success",
                "headers": ["ID (int)", "Code (smallint)", "Score (float)", "Name (char 50)"],
                "records": records
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def parse_csv_file(file_path: str) -> Dict[str, Any]:
        """
        Парсер CSV-файлов для отображения в таблице DataTables.
        """
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader, [])
                rows = [row for row in reader]
            return {"status": "success", "headers": headers, "rows": rows}
        except Exception as e:
            return {"status": "error", "message": str(e)}