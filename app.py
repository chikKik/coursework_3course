from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Словарь с данными для пересчета
CONVERSION_DATA = {
    # Лабораторные анализы крови
    "Глюкоза": {
        "unit1": "мг/дл",
        "unit2": "ммоль/л",
        "factor": 0.0555,
        "formula": "ммоль/л = мг/дл × 0.0555"
    },
    "Холестерин общий": {
        "unit1": "мг/дл",
        "unit2": "ммоль/л",
        "factor": 0.02586,
        "formula": "ммоль/л = мг/дл × 0.02586"
    },
    "Холестерин ЛПНП": {
        "unit1": "мг/дл",
        "unit2": "ммоль/л",
        "factor": 0.02586,
        "formula": "ммоль/л = мг/дл × 0.02586"
    },
    "Холестерин ЛПВП": {
        "unit1": "мг/дл",
        "unit2": "ммоль/л",
        "factor": 0.02586,
        "formula": "ммоль/л = мг/дл × 0.02586"
    },
    "Триглицериды": {
        "unit1": "мг/дл",
        "unit2": "ммоль/л",
        "factor": 0.01129,
        "formula": "ммоль/л = мг/дл × 0.01129"
    },
    "Креатинин": {
        "unit1": "мг/дл",
        "unit2": "мкмоль/л",
        "factor": 88.4,
        "formula": "мкмоль/л = мг/дл × 88.4"
    },
    "Мочевина": {
        "unit1": "мг/дл",
        "unit2": "ммоль/л",
        "factor": 0.1664,
        "formula": "ммоль/л = мг/дл × 0.1664"
    },
    "Мочевая кислота": {
        "unit1": "мг/дл",
        "unit2": "мкмоль/л",
        "factor": 59.48,
        "formula": "мкмоль/л = мг/дл × 59.48"
    },
    "Билирубин общий": {
        "unit1": "мг/дл",
        "unit2": "мкмоль/л",
        "factor": 17.1,
        "formula": "мкмоль/л = мг/дл × 17.1"
    },
    "Железо сыворотки": {
        "unit1": "мкг/дл",
        "unit2": "мкмоль/л",
        "factor": 0.179,
        "formula": "мкмоль/л = мкг/дл × 0.179"
    },
    "Кальций": {
        "unit1": "мг/дл",
        "unit2": "ммоль/л",
        "factor": 0.2495,
        "formula": "ммоль/л = мг/дл × 0.2495"
    },
    "Натрий": {
        "unit1": "мэкв/л",
        "unit2": "ммоль/л",
        "factor": 1.0,
        "formula": "ммоль/л = мэкв/л × 1.0 (1:1)"
    },
    "Калий": {
        "unit1": "мэкв/л",
        "unit2": "ммоль/л",
        "factor": 1.0,
        "formula": "ммоль/л = мэкв/л × 1.0 (1:1)"
    },
    
    # Витамины
    "Витамин A (Ретинол)": {
        "unit1": "мкг/дл",
        "unit2": "мкмоль/л",
        "factor": 0.0349,
        "formula": "мкмоль/л = мкг/дл × 0.0349"
    },
    "Витамин B12 (Кобаламин)": {
        "unit1": "пг/мл",
        "unit2": "пмоль/л",
        "factor": 0.738,
        "formula": "пмоль/л = пг/мл × 0.738"
    },
    "Витамин C (Аскорбиновая кислота)": {
        "unit1": "мг/дл",
        "unit2": "мкмоль/л",
        "factor": 56.78,
        "formula": "мкмоль/л = мг/дл × 56.78"
    },
    "Витамин D (25-гидрокси)": {
        "unit1": "нг/мл",
        "unit2": "нмоль/л",
        "factor": 2.496,
        "formula": "нмоль/л = нг/мл × 2.496"
    },
    "Витамин E (Токоферол)": {
        "unit1": "мг/дл",
        "unit2": "мкмоль/л",
        "factor": 23.22,
        "formula": "мкмоль/л = мг/дл × 23.22"
    },
    "Витамин K": {
        "unit1": "нг/мл",
        "unit2": "нмоль/л",
        "factor": 2.22,
        "formula": "нмоль/л = нг/мл × 2.22"
    },
    "Фолиевая кислота (Витамин B9)": {
        "unit1": "нг/мл",
        "unit2": "нмоль/л",
        "factor": 2.266,
        "formula": "нмоль/л = нг/мл × 2.266"
    }
}


@app.route('/')
def index():
    """Главная страница с формой для пересчета"""
    tests = list(CONVERSION_DATA.keys())
    # ВАЖНО: передаём обе переменные в шаблон
    return render_template('index.html', tests=tests, conversion_data=CONVERSION_DATA)


@app.route('/convert', methods=['POST'])
def convert():
    """API для конвертации единиц измерения"""
    try:
        test_name = request.form.get('test_name')
        value = request.form.get('value')
        
        if not test_name or not value:
            return jsonify({'error': 'Пожалуйста, заполните все поля'}), 400
        
        try:
            value_float = float(value)
        except ValueError:
            return jsonify({'error': 'Введите корректное числовое значение'}), 400
        
        test_data = CONVERSION_DATA.get(test_name)
        if not test_data:
            return jsonify({'error': 'Показатель не найден'}), 400
        
        converted_value = value_float * test_data['factor']
        
        if abs(converted_value) < 0.01:
            rounded = round(converted_value, 4)
        elif abs(converted_value) < 10:
            rounded = round(converted_value, 2)
        else:
            rounded = round(converted_value, 1)
        
        result = {
            'test_name': test_name,
            'original_value': value_float,
            'original_unit': test_data['unit1'],
            'converted_value': rounded,
            'converted_unit': test_data['unit2'],
            'formula': test_data['formula'],
            'factor': test_data['factor']
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Произошла ошибка: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)