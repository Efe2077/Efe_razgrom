from pytrovich.maker import NamePart, Gender, Case, PetrovichDeclinationMaker
import pymorphy3


def get_fio(teacher_fio):
    full_name = teacher_fio.split()
    name = full_name[1]
    surname = full_name[0]
    patronymic = full_name[-1]

    if patronymic == name:
        patronymic = ''

    morph = pymorphy3.MorphAnalyzer()
    morph = morph.parse(name)[0]
    gender = morph.tag.gender

    maker = PetrovichDeclinationMaker()

    if gender == 'femn':
        im_name = surname.capitalize()
        ac_name = maker.make(NamePart.LASTNAME, Gender.FEMALE, Case.ACCUSATIVE, surname).capitalize()
        gen_name = maker.make(NamePart.LASTNAME, Gender.FEMALE, Case.GENITIVE, surname).capitalize()
        dat_name = maker.make(NamePart.LASTNAME, Gender.FEMALE, Case.DATIVE, surname).capitalize()
        a = [im_name, ac_name, gen_name, dat_name]
        answer = []
        for el in a:
            r = f'{el} {name[0].upper()}.'
            if patronymic:
                r += f'{patronymic[0].upper()}.'
            answer.append(r)
        return answer
    else:
        im_name = surname.capitalize()
        ac_name = maker.make(NamePart.LASTNAME, Gender.MALE, Case.ACCUSATIVE, surname).capitalize()
        gen_name = maker.make(NamePart.LASTNAME, Gender.MALE, Case.GENITIVE, surname).capitalize()
        dat_name = maker.make(NamePart.LASTNAME, Gender.MALE, Case.DATIVE, surname).capitalize()
        a = [im_name, ac_name, gen_name, dat_name]
        answer = []
        for el in a:
            r = f'{el} {name[0].upper()}.'
            if patronymic:
                r += f'{patronymic[0].upper()}.'
            answer.append(r)
        return answer