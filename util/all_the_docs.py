import Urlsnatcher
import pdfmaker
import cik

for tick in cik.get_tickers()[75:]:
    print(f'{tick} old')
    user_data = {'tick': tick, 'form': '10-K', 'range': ('18', '22')}
    urls = Urlsnatcher.get_url(user_data['tick'], user_data['form'], user_data['range'])
    name = pdfmaker.make_pdf(urls, user_data)
