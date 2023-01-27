def create_txt(user, ingredients_value):
    """Создание txt-файла."""
    first_string = (
        f'Пользователь {user.get_full_name()} \n\n'
    )
    shoping_list = '\n'.join([f'{ing["ingredient__name"]} '
                              f'{ing["amount"]} '
                              f'{ing["ingredient__measurement_unit"]}'
                              for ing in ingredients_value])
    footer = '\n\n\nFoodgram project'

    ready_list = first_string + shoping_list + footer
    filename = f'{user.username}_shopping_list.txt'
    return ready_list, filename
