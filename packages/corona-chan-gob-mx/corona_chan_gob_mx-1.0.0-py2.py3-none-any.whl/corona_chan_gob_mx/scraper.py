import camelot
from PyPDF2 import PdfFileReader
from chibi.file.temp import Chibi_temp_path
from chibi.snippet.string import remove_inner_space
from chibi_requests import Chibi_url, Response


def pdf_to_dicts( pdf ):
    pdf_reader = PdfFileReader( pdf )
    tables = camelot.read_pdf(
        pdf, pages=f"1-{pdf_reader.numPages}", split_text=True )
    name_headers = {
        "edad": "age",
        "estado": "state",
        "fecha de inicio de síntomas": "symptom_start_date",
        "fecha del llegada a méxico": "arrive_date_to_mexico",
        "identificación de covid-19 por rt-pcr en tiempo real": "status",
        "n° caso": "number_case",
        "procedencia": "arrive_from",
        "sexo": "sex",
    }
    dataframes = [ t.df for t in tables ]
    headers = [
        name_headers[ remove_inner_space( dataframes[0][:1][i][0] ).lower() ]
        for i in range( len( dataframes[0].keys() ) ) ]
    dataframes[0] = dataframes[0][1:]
    result = []
    for df in dataframes:
        series_tmp = [ df[i] for i, k in enumerate( headers ) ]
        for series in zip( *series_tmp ):
            current = { k.lower(): series[i] for i, k in enumerate( headers ) }
            result.append( current )
    return result


class Find_pdfs( Response ):
    def parse_native( self ):
        native = super().parse_native()
        links = map(
            lambda a: a.attrs.get( 'href', '' ),
            native.find_all( 'a' ), )
        links = filter( lambda a: a.endswith( '.pdf' ), links )
        links = map( lambda link: Pdf_url( self.url + link ), links )
        links = filter(
            lambda link: link.base_name.startswith( 'Tabla_casos' ),
            links )
        return list( links )


class Pdf_url( Chibi_url ):
    def get( self, *args, **kw ):
        temp_dir = Chibi_temp_path()
        pdf = self.download( temp_dir )

        data = pdf_to_dicts( pdf )
        response = Response( response=object(), url=self )
        response._native = data
        return response


list_of_pdf = Chibi_url(
    "https://www.gob.mx/salud/documentos/"
    "coronavirus-covid-19-comunicado-tecnico-diario-238449",
    response_class=Find_pdfs )
