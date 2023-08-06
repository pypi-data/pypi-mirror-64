import time
import shutil
import typing
import urllib.parse
import urllib.error
import urllib.request
import multiprocessing.pool

from .termcolor import *

from bs4 import BeautifulSoup


class Downink(object):
    def __init__(
        self,
        url: str,
        single: bool = False,
        class_names: typing.List[str] = None,
        expressions: typing.List[str] = None,
    ) -> None:

        self.start_time = time.time()

        if single:
            if url.count('/') >= 3:
                name = url.rsplit('/', 1)[1]
            else:
                name = ''
            self._download((name, url))

        self.expressions = expressions
        self.class_names = class_names
        self._url = url if not url.endswith('/') else url[:-1]

        self.url = urllib.parse.urlparse(self._url)

        self.dir_name = self.url.hostname + ' files/'

        try:
            os.mkdir(self.dir_name)
        except FileExistsError:
            shutil.rmtree(self.dir_name)
            os.mkdir(self.dir_name)

        try:
            with urllib.request.urlopen(self._url) as response:
                self.html = response.read()
        except urllib.error.URLError:
            print_error('please check your network connection')

        self.soup: BeautifulSoup = BeautifulSoup(self.html, 'html.parser')

        self.name_and_links: typing.Set = set()
        if len(self.expressions) == 0 and len(self.class_names) == 0:
            print_error('required expressions or class names')
        if self.expressions:
            self._get_links_from_expressions()
        if self.class_names:
            self._get_links_from_classes()
        self.start_downloads()

    def _extract_href_and_text(
        self, element, pre_text: str = None
    ) -> typing.Tuple[str, str]:
        if element.name == 'a':
            href: str = element.get('href')
            if not (
                href.startswith('https://')
                or href.startswith('http://')
                or href.startswith('//')
            ):
                # href is not an absolute url
                if href.startswith('/'):
                    # href is internal absolute
                    href = '{}://{}{}'.format(self.url.scheme, self.url.hostname, href)
                else:
                    # href is local
                    href = '{}://{}'.format(self.url.scheme, href)
            if not pre_text:
                pre_text = element.text.replace('\n', ' ')
            return pre_text, href
        else:
            return self._extract_href_and_text(
                element.find('a'), element.text.replace('\n', ' ')
            )

    def _get_links_from_classes(self):
        for class_name in self.class_names:
            for elem in self.soup.find_all(attrs={'class': class_name}):
                self.name_and_links.add(self._extract_href_and_text(elem))

    def _get_links_from_expressions(self):
        for expression in self.expressions:
            for elem in self.soup.find_all('a', string=re.compile(expression)):
                self.name_and_links.add(self._extract_href_and_text(elem))

    def _download(self, name_and_link) -> typing.Tuple[bool, str]:
        try:
            name, link = name_and_link
            with urllib.request.urlopen(link) as response:
                f = open(self.dir_name + name, 'wb+')
                f.write(response.read())
                f.close()
        except Exception as e:
            return False, str(e)
        else:
            return True, ''

    def start_downloads(self):
        counter = 0
        print_info('starting download')
        results = multiprocessing.pool.ThreadPool(10).imap_unordered(
            self._download, self.name_and_links
        )
        try:
            for success, err in results:
                if not success:
                    print()
                    print_error("couldn't download files")
                else:
                    counter += 1
                    index = (counter % 4) + 1
                    slash = '|/-\\|'[index]
                    print_progress(
                        'receiving {}/{} files  [{}]    '.format(
                            counter, len(self.name_and_links), slash
                        ),
                        slash,
                    )
        except (KeyboardInterrupt, EOFError):
            print()
            print_error('interrupted. goodbye.')
        except Exception as e:
            print()
            print_error(str(e))
        else:
            print()
            print_info(
                'saved {} files to "{}"'.format(len(self.name_and_links), self.dir_name)
            )
            end_time = time.time()
            print_success(
                'finished in {} seconds'.format(round(end_time - self.start_time, 3))
            )
