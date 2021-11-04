import json
import re
import time

import xmltodict
import xml.etree.ElementTree as ET

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from datetime import datetime

from bin.Aprobacion import Aprobacion
from bin.Autorizacion import Autorizacion
from bin.Codigo import Codigo
from bin.DTE import DTE
from bin.Duplicado import Duplicado
from bin.Errores import Errores
from lista.Lista import Lista

app = Flask(__name__)
cors = CORS(app, resource={r'/*': {"origin": "*"}})

listaDTE = Lista()
listaAutorizacion = Lista()
codigo = Codigo()


@app.route('/procesar', methods=['POST'])
def procesar():
    response = json.loads(json.dumps(xmltodict.parse(request.data)))

    SOLICITUD_AUTORIZACION = response['SOLICITUD_AUTORIZACION']['DTE']

    for temp in SOLICITUD_AUTORIZACION:
        listaDTE.agregar(DTE(
            temp['TIEMPO'],
            temp['REFERENCIA'],
            temp['NIT_EMISOR'],
            temp['NIT_RECEPTOR'],
            temp['VALOR'],
            temp['IVA'],
            temp['TOTAL']
        ))

    resumenDatos()

    return Response(status=200)


@app.route('/procesar', methods=['GET'])
def procesar_get():
    if listaDTE.getCantidad() != 0:
        data = ET.Element("DATOS")
        aux = listaDTE.getLista()
        while aux:
            _dte = ET.SubElement(data, 'DTE')

            _tiempo = ET.SubElement(_dte, 'TIEMPO')
            _dia = ET.SubElement(_tiempo, 'DIA')
            _dia.text = str(aux.dato.getFecha().getDia())
            _hora = ET.SubElement(_tiempo, 'HORA')
            _hora.text = str(aux.dato.getFecha().getHora())

            _referencia = ET.SubElement(_dte, 'REFERENCIA')
            _referencia.text = str(aux.dato.getReferencia())

            _nitE = ET.SubElement(_dte, 'NIT_EMISOR')
            _nitE.text = str(aux.dato.getNitEmisor())

            _nitR = ET.SubElement(_dte, 'NIT_RESEPTOR')
            _nitE.text = str(aux.dato.getNitReseptor())

            _valor = ET.SubElement(_dte, 'VALOR')
            _valor.text = str(aux.dato.getValor())

            _iva = ET.SubElement(_dte, 'IVA')
            _iva.text = str(aux.dato.getIva())

            _total = ET.SubElement(_dte, 'TOTAL')
            _total.text = str(aux.dato.getTotal())

            aux = aux.siguiente
            if aux == listaDTE.primero:
                break

        data = json.dumps(xmltodict.parse(ET.tostring(data)))
        return Response(status=200, response=data)
    else:
        return Response(status=204)


@app.route('/resumenRango/<string:tipo>/<string:fecha1>/<string:fecha2>', methods=['GET'])
def resumenRango(fecha1, fecha2, tipo):
    if listaAutorizacion.getCantidad() != 0:
        tempAu = Lista()
        aux1 = listaAutorizacion.getLista()
        while aux1:
            aux2 = aux1.dato.getListaAprobacion().getLista()
            while aux2:
                aux3 = listaDTE.getLista()
                while aux3:
                    if aux2.dato.getReferencia() == aux3.dato.getReferencia():
                        tempAu.agregar(aux3.dato)
                        break

                    aux3 = aux3.siguiente
                    if aux3 == listaDTE.primero:
                        break

                aux2 = aux2.siguiente
                if aux2 == aux1.dato.getListaAprobacion().getLista():
                    break

            aux1 = aux1.siguiente
            if aux1 == listaAutorizacion.primero:
                break

        data = ET.Element('DATOS')
        aux = tempAu.getLista()

        contador = 1
        if int(tipo) == 1:
            while aux:
                if validarFechaRango(fecha1.replace('-', '/'), fecha2.replace('-', '/'), aux.dato.getFecha().getDia()):
                    _factura = ET.SubElement(data, 'FACTURA')

                    _nit = ET.SubElement(_factura, 'NIT_EMISOR')
                    _nit.text = str(aux.dato.getNitEmisor())

                    _monto = ET.SubElement(_factura, 'MONTO')
                    _monto.text = str(aux.dato.getValor())

                    _fecha = ET.SubElement(_factura, 'FECHA')
                    _fecha.text = str(aux.dato.getFecha().getDia())

                    _cont = ET.SubElement(_factura, 'NO')
                    _cont.text = str(contador)
                    contador += 1

                aux = aux.siguiente
                if aux == tempAu.primero:
                    break

            if json.loads(json.dumps(xmltodict.parse(ET.tostring(data))))['DATOS'] is not None:
                return Response(status=200, response=json.dumps(xmltodict.parse(ET.tostring(data))))
            else:
                return Response(status=205)
        elif int(tipo) == 2:
            while aux:
                if validarFechaRango(fecha1.replace('-', '/'), fecha2.replace('-', '/'), aux.dato.getFecha().getDia()):
                    _factura = ET.SubElement(data, 'FACTURA')

                    _nit = ET.SubElement(_factura, 'NIT_EMISOR')
                    _nit.text = str(aux.dato.getNitEmisor())

                    _monto = ET.SubElement(_factura, 'MONTO')
                    _monto.text = str(float(aux.dato.getValor()) * 1.12)

                    _fecha = ET.SubElement(_factura, 'FECHA')
                    _fecha.text = str(aux.dato.getFecha().getDia())

                    _cont = ET.SubElement(_factura, 'NO')
                    _cont.text = str(contador)
                    contador += 1

                aux = aux.siguiente
                if aux == tempAu.primero:
                    break

            if json.loads(json.dumps(xmltodict.parse(ET.tostring(data))))['DATOS'] is not None:
                return Response(status=200, response=json.dumps(xmltodict.parse(ET.tostring(data))))
            else:
                return Response(status=205)
        else:
            return Response(status=205)
    else:
        return Response(status=204)


@app.route('/resumenIva/<string:fecha>', methods=['GET'])
def resumenIva(fecha):
    if listaAutorizacion.getCantidad() != 0:
        tempAu = Lista()
        aux1 = listaAutorizacion.getLista()
        while aux1:
            aux2 = aux1.dato.getListaAprobacion().getLista()
            while aux2:
                aux3 = listaDTE.getLista()
                while aux3:
                    if aux2.dato.getReferencia() == aux3.dato.getReferencia():
                        tempAu.agregar(aux3.dato)
                        break

                    aux3 = aux3.siguiente
                    if aux3 == listaDTE.primero:
                        break

                aux2 = aux2.siguiente
                if aux2 == aux1.dato.getListaAprobacion().getLista():
                    break

            aux1 = aux1.siguiente
            if aux1 == listaAutorizacion.primero:
                break

        data = ET.Element('DATOS')
        aux = tempAu.getLista()
        while aux:
            if validarFecha(fecha.replace('-', '/'), aux.dato.getFecha().getDia()):
                _factura = ET.SubElement(data, 'FACTURA')

                _nit = ET.SubElement(_factura, 'NIT_EMISOR')
                _nit.text = str(aux.dato.getNitEmisor())

                _monto = ET.SubElement(_factura, 'MONTO')
                _monto.text = str(aux.dato.getValor())

                _fecha = ET.SubElement(_factura, 'FECHA')
                _fecha.text = str(aux.dato.getFecha().getDia())

                _iva = ET.SubElement(_factura, 'IVA')
                _iva.text = str(float(aux.dato.getValor()) * 0.12)

            aux = aux.siguiente
            if aux == tempAu.primero:
                break

        if json.loads(json.dumps(xmltodict.parse(ET.tostring(data))))['DATOS'] is not None:
            return Response(status=200, response=json.dumps(xmltodict.parse(ET.tostring(data))))
        else:
            return Response(status=205)
    else:
        return Response(status=204)


@app.route('/consultaDatos', methods=['GET'])
def resumenDatos():
    if listaDTE.getCantidad() != 0:
        listaAutorizacion.vaciar()

        facturasRecibidas = numeroFacturas()
        listaErroresFacturas = erroresFacturas()

        facturasCorrectas = 0
        tempDuplicados = Lista()
        aux1 = listaErroresFacturas.primero
        while aux1:
            error = aux1.dato
            if tempDuplicados.getCantidad() != 0:
                aux2 = tempDuplicados.primero
                while aux2:
                    if aux1.dato.getReferencia() == aux2.dato.getReferencia():
                        aux2.dato.setCantidad()
                        break
                    aux2 = aux2.siguiente
                    if aux2 == tempDuplicados.primero:
                        tempDuplicados.agregar(Duplicado(aux1.dato.getReferencia()))
                        break
            else:
                tempDuplicados.agregar(Duplicado(error.getReferencia()))
            aux1 = aux1.siguiente
            if aux1 == listaErroresFacturas.primero:
                break

        listaAprobacion = Lista()
        aux1 = listaDTE.primero
        while aux1:
            if tempDuplicados.getCantidad() != 0:
                aux2 = tempDuplicados.primero
                while aux2:
                    if aux1.dato.getReferencia() == aux2.dato.getReferencia():
                        break

                    aux2 = aux2.siguiente
                    if aux2 == tempDuplicados.primero:
                        facturasCorrectas += 1
                        codigo.uso()
                        listaAprobacion.agregar(
                            Aprobacion(aux1.dato.getNitEmisor(), aux1.dato.getReferencia(), codigo.getCodigo(),
                                       aux1.dato.getFecha()))
                        break
            else:
                facturasCorrectas += 1
                codigo.uso()
                listaAprobacion.agregar(
                    Aprobacion(aux1.dato.getNitEmisor(), aux1.dato.getReferencia(), codigo.getCodigo(),
                               aux1.dato.getFecha()))

            aux1 = aux1.siguiente
            if aux1 == listaDTE.primero:
                break

        autorizacion = Autorizacion(facturasRecibidas, facturasCorrectas, cantidadEmisores(), cantidadReceptores())
        aux = listaErroresFacturas.primero
        while aux:
            autorizacion.agregarError(aux.dato.getEtiqueta(), aux.dato.getValor(), aux.dato.getReferencia())
            aux = aux.siguiente
            if aux == listaErroresFacturas.primero:
                break
        aux = listaAprobacion.primero
        while aux:
            autorizacion.agregarAprovacion(aux.dato.getNit(), aux.dato.getReferencia(), aux.dato.getCodigo(),
                                           aux.dato.getFecha())
            aux = aux.siguiente
            if aux == listaAprobacion.primero:
                break
        listaAutorizacion.agregar(autorizacion)

        data = ET.Element('LISTAAUTORIZACIONES')
        aux1 = listaAutorizacion.getLista()
        while aux1:
            _autorizacion = ET.SubElement(data, 'AUTORIZACION')

            _fecha = ET.SubElement(_autorizacion, 'FECHA')
            _fecha.text = str(aux1.dato.getFecha())

            _facturas = ET.SubElement(_autorizacion, 'FACTURAS_RECIBIDAS')
            _facturas.text = str(aux1.dato.getFacturas())

            _errores = ET.SubElement(_autorizacion, 'ERRORES')
            if aux1.dato.getListaErrores().getCantidad() != 0:
                aux2 = aux1.dato.getListaErrores().getLista()
                while aux2:
                    _error = ET.SubElement(_errores, str(aux2.dato.getEtiqueta()))
                    _error.text = str(aux2.dato.getValor())
                    if aux2.dato.getReferencia() is not None:
                        _error.set("ref", str(aux2.dato.getReferencia()))

                    aux2 = aux2.siguiente
                    if aux2 == aux1.dato.getListaErrores().primero:
                        break

            _correctas = ET.SubElement(_autorizacion, 'FACTURAS_CORRECTAS')
            _correctas.text = str(facturasCorrectas)

            _cEmisores = ET.SubElement(_autorizacion, 'CANTIDAD_EMISORES')
            _cEmisores.text = str(cantidadEmisores())

            _cReceptores = ET.SubElement(_autorizacion, 'CANTIDAD_RECEPTORES')
            _cReceptores.text = str(cantidadReceptores())

            _listaA = ET.SubElement(_autorizacion, 'LISTADO_AUTORIZACIONES')
            if listaAprobacion.getCantidad() != 0:
                aux2 = listaAprobacion.getLista()
                while aux2:
                    _aprobacion = ET.SubElement(_listaA, 'APROBACION')

                    _nitEmisor = ET.SubElement(_aprobacion, 'NIT_EMISOR')
                    _nitEmisor.set('ref', str(aux2.dato.getReferencia()))
                    _nitEmisor.text = str(aux2.dato.getNit())

                    _fecha = ET.SubElement(_aprobacion, 'FECHA')
                    _dia = ET.SubElement(_fecha, 'DIA')
                    _dia.text = str(aux2.dato.getFecha().getDia())
                    _hora = ET.SubElement(_fecha, 'HORA')
                    _hora.text = str(aux2.dato.getFecha().getHora())

                    _codigo = ET.SubElement(_aprobacion, 'CODIGO_APROBACION')
                    _codigo.text = str(aux2.dato.getCodigo())

                    aux2 = aux2.siguiente
                    if aux2 == listaAprobacion.primero:
                        break

            _totalA = ET.SubElement(_listaA, 'TOTAL_APROBACIONES')
            _totalA.text = str(aux1.dato.getTotalAprobacion())

            aux1 = aux1.siguiente
            if aux1 == listaAutorizacion.primero:
                break
        return Response(status=200, response=ET.tostring(data))
    else:
        return Response(status=204)


@app.route('/borrar', methods=['PUT'])
def borrar():
    listaDTE.vaciar()
    listaAutorizacion.vaciar()
    codigo.reinicar()

    return Response(status=200)


@app.route('/nit', methods=['GET'])
def obtenerNit():
    if listaAutorizacion.getCantidad() != 0:
        data = ET.Element('DATOS')

        aux1 = listaAutorizacion.getLista()
        while aux1:
            aux2 = aux1.dato.getListaAprobacion().getLista()
            while aux2:
                nit = ET.SubElement(data, 'NIT')
                nit.text = str(aux2.dato.getNit())
                aux2 = aux2.siguiente
                if aux2 == aux1.dato.getListaAprobacion().primero:
                    break

            aux1 = aux1.siguiente
            if aux1 == listaAutorizacion.primero:
                break

        return json.dumps(xmltodict.parse(ET.tostring(data)))
    else:
        return jsonify({'mensaje': 204})


def validarNit(numero):
    temp = 1
    numero = str(numero)[::-1]
    total1 = 0

    while temp < len(numero):
        total1 = total1 + (int(numero[temp]) * (temp + 1))
        temp += 1

    total2 = total1 - ((total1 // 11) * 11)
    total3 = 11 - (total2 - (total2 * (total2 // 11)))

    return total3 == int(numero[0])


def validarIVA(monto, iva):
    return "{:.2f}".format(float(float(monto) * 0.12)) == "{:.2f}".format(float(iva))


def validarTotal(total, monto):
    return "{:.2f}".format(float(total)) == "{:.2f}".format(float(monto) * 1.12)


def numeroFacturas():
    return listaDTE.getCantidad()


def erroresFacturas():
    tempErrores = Lista()

    aux1 = listaDTE.primero
    while aux1:
        dte = aux1.dato
        if not validarNit(dte.getNitEmisor()):
            tempErrores.agregar(Errores("NIT_EMISOR", dte.getNitEmisor(), dte.getReferencia()))
        if not validarNit(dte.getNitReseptor()):
            tempErrores.agregar(Errores("NIT_RECEPTOR", dte.getNitReseptor(), dte.getReferencia()))
        if not validarIVA(dte.getValor(), dte.getIva()):
            tempErrores.agregar(Errores("IVA", dte.getIva(), dte.getReferencia()))
        if not validarTotal(dte.getTotal(), dte.getValor()):
            tempErrores.agregar(Errores("TOTAL", dte.getTotal(), dte.getReferencia()))

        dia = hora = 0

        if re.search('\d+\/{1}\d+\/{1}\d+', dte.getTiempo()) is not None:
            dia = re.search('\d+\/{1}\d+\/{1}\d+', dte.getTiempo()).group(0)
            try:
                datetime.strptime(str(dia), '%d/%m/%Y')
            except ValueError:
                tempErrores.agregar(Errores("TIEMPO", dte.getTotal(), dte.getReferencia()))
        else:
            tempErrores.agregar(Errores("TIEMPO", dte.getTotal(), dte.getReferencia()))

        if re.search('([0]{0,1}[1-9]{1}|[1]{1}[0-9]{1}|[2]{1}[0-4]{1}){1}\:{1}[0-5]{1}[0-9]{1}',
                     dte.getTiempo()) is not None:
            hora = re.search('([0]{0,1}[1-9]{1}|[1]{1}[0-9]{1}|[2]{1}[0-4]{1}){1}\:{1}[0-5]{1}[0-9]{1}',
                             dte.getTiempo()).group(0)
        else:
            tempErrores.agregar(Errores("TIEMPO", dte.getTotal(), dte.getReferencia()))

        if dia != 0 and hora != 0:
            dte.crearFecha(dia, hora)

        aux1 = aux1.siguiente
        if aux1 == listaDTE.primero:
            break

    duplicados = validarReferencia()
    totalDuplicadas = 0
    aux1 = duplicados.primero
    while aux1:
        if aux1.dato.getCantidad() != 1:
            totalDuplicadas += 1
        aux1 = aux1.siguiente
        if aux1 == duplicados.primero:
            break

    if totalDuplicadas != 0:
        tempErrores.agregar(Errores("REFERENCIAS_DUPLICADAS", totalDuplicadas, None))
    return tempErrores


def validarReferencia():
    duplicados = Lista()

    aux1 = listaDTE.primero
    while aux1:
        if duplicados.getCantidad() != 0:
            aux2 = duplicados.primero
            while aux2:
                if aux1.dato.getReferencia() == aux2.dato.getReferencia():
                    aux2.dato.setCantidad()
                    break
                aux2 = aux2.siguiente
                if aux2 == duplicados.primero:
                    duplicados.agregar(Duplicado(aux1.dato.getReferencia()))
                    break
        else:
            duplicados.agregar(Duplicado(aux1.dato.getReferencia()))
        aux1 = aux1.siguiente
        if aux1 == listaDTE.primero:
            break

    return duplicados


def cantidadEmisores():
    tempEmisores = Lista()

    aux1 = listaDTE.primero
    while aux1:
        if tempEmisores.getCantidad() != 0:
            aux2 = tempEmisores.primero
            while aux2:
                if aux1.dato.getNitEmisor() == aux2.dato.getReferencia():
                    aux2.dato.setCantidad()
                    break
                aux2 = aux2.siguiente
                if aux2 == tempEmisores.primero:
                    tempEmisores.agregar(Duplicado(aux1.dato.getNitEmisor()))
                    break
        else:
            tempEmisores.agregar(Duplicado(aux1.dato.getNitEmisor()))
        aux1 = aux1.siguiente
        if aux1 == listaDTE.primero:
            break

    return tempEmisores.getCantidad()


def cantidadReceptores():
    tempReceptores = Lista()

    aux1 = listaDTE.primero
    while aux1:
        if tempReceptores.getCantidad() != 0:
            aux2 = tempReceptores.primero
            while aux2:
                if aux1.dato.getNitReseptor() == aux2.dato.getReferencia():
                    aux2.dato.setCantidad()
                    break
                aux2 = aux2.siguiente
                if aux2 == tempReceptores.primero:
                    tempReceptores.agregar(Duplicado(aux1.dato.getNitReseptor()))
                    break
        else:
            tempReceptores.agregar(Duplicado(aux1.dato.getNitReseptor()))
        aux1 = aux1.siguiente
        if aux1 == listaDTE.primero:
            break

    return tempReceptores.getCantidad()


def validarFecha(mayor, menor):
    return time.strptime(mayor, "%d/%m/%Y") == time.strptime(str(menor), "%d/%m/%Y")


def validarFechaRango(r1, r2, fecha):
    return time.strptime(r1, "%d/%m/%Y") <= time.strptime(fecha, "%d/%m/%Y") <= time.strptime(r2, "%d/%m/%Y")


if __name__ == '__main__':
    app.run()
