from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa


class Render:

	@staticmethod

	def render(path: str, params: dict):
		template = get_template(path)
		html = template.render(params)
		#response = BytesIO()
		#pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
		response = HttpResponse(content_type='application/pdf')
		#response['Content-disposition'] = 'attachment; filename="dokument.pdf"'
		pdf = pisa.CreatePDF(html, dest=response)
		if not pdf.err:
			#return HttpResponse(response.getvalue(), content_type='application/pdf')
			return response
		else:
			return HttpResponse('Error Rendering PDF', status=400)	
