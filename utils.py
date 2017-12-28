# -*- coding: utf-8 -*-


def elimina_tildes(palabra):
    palabra = palabra.replace('á', 'a')
    palabra = palabra.replace('é', 'e')
    palabra = palabra.replace('í', 'i')
    palabra = palabra.replace('ó', 'o')
    palabra = palabra.replace('ú', 'u')
    return palabra


def elimina_caracteres_especiales(palabra):
    borrandoCaracterEspecial = palabra.translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
    if borrandoCaracterEspecial == ' ':
        return ''
    return borrandoCaracterEspecial

#print(elimina_caracteres_especiales(')'))

