from genshi.builder import tag
from genshi.filters import Transformer
from genshi.input import XML

from trac.core import *
from trac.wiki.macros import WikiMacroBase
from trac.mimeview.api import Mimeview
from trac.wiki.api import parse_args
from trac.versioncontrol.api import RepositoryManager

try:
    from trac.versioncontrol.api import IRepositoryProvider
    multirepos = True
except:
    multirepos = False

class IncludeSourceMacro(WikiMacroBase):
    """Includes a source file from the repository into the Wiki.

    There is one required parameter, which is the path to the
    file to include. This should be the repository path, not a
    full URL.

    Optional named parameters are:
     * ''start '' The first line of the file to include. Defaults to the
     beginning of the file. Otherwise should be a numeric value.

     Note that files start with line 1, not line 0.
     * ''end'' The last line of the file to include. Defaults to the end
     of the file.

     Note that both 'start' and 'end' are used for array slicing the
     lines of the file, so if (for example) you want the last 20 lines
     of the file, you can use start=-20 and leave end blank.
     * ''rev'' Which revision to include. This defaults to HEAD if
     not supplied. Otherwise this should be a valid numeric revision
     number in your version control repository.
     * ''mimetype'' Which mimetype to use to determine syntax highlighting.
     If not supplied, this is determined by the file extension (which
     is normally what you want)

    Examples:
    {{{
        # include entire file
        [[IncludeSource(trunk/proj/file.py)]]

        # includes line 20-50 inclusive
        [[IncludeSource(trunk/proj/file.py, start=20, end=50)]]

        # includes last 30 lines of file at revision 1200
        [[IncludeSource(trunk/proj/file.py, start=-30, rev=1200)]]

        # include entire file but formatted plain
        [[IncludeSource(trunk/proj/file.py, mimetype=text/plain)]]

        # includes line 20-50 inclusive and overrides file name link
        # in header text
        [[IncludeSource(trunk/proj/file.py, start=20, end=50, header=New header text)]]

        # includes line 20-50 inclusive and overrides file name link
        # in header text, along with a specific CSS class (class must exist
        # in CSS on page; there is no provision for defining it in this macro)
        [[IncludeSource(trunk/proj/file.py, start=20, end=50, header=New header text, header_class=my_class)]]

        # includes line 20-50 inclusive, but suppresses the display of line numbers.
        # (0, no, false, and none are all honored for suppressing - case insensitive)
        [[IncludeSource(trunk/proj/file.py, start=20, end=50, line_numbers=0)]]

    }}}

    See TracLinks, TracSyntaxColoring and trac/mimeview/api.py

    TODO
    {{{
    * Fix non-localized strings

    * Fix proper encoding of output

    * Implement some sort of caching (especially in cases where the
    revision is known and we know that the contents won't change).

    * Allow multiple chunks from the file in one call. You can do this
    with the existing code, but it will pull the entire file out of
    version control and trim it for each chunk, so this could be
    optimized a bit.  This could be done with the Ranges object

    * Refactor code a bit - there are enough special cases in it now
    that the expand_macro call is getting a bit unwieldy.

    }}}
    """

    def expand_macro(self, formatter, name, content):
        self.log.info('Begin expand_macro for req: ' + repr(content))
        largs, kwargs = parse_args(content)
        href = formatter.href

        if len(largs) == 0:
            raise TracError("File name to include is required parameter!")

        orig_file_name = file_name = largs[0]

        rm = RepositoryManager(self.env)
        global multirepos
        if not multirepos:
            repos = rm(formatter.req.authname)
        else:
            if (orig_file_name[0] == '/'): orig_file_name = orig_file_name[1:]
            splitpath = file_name.split('/')
            if (file_name[0] == '/'):
                reponame = splitpath[1]
            else:
                reponame = splitpath[0]
            repos = rm.get_repository(reponame)
            if (repos):
                l = len(reponame)
                if (file_name[0] == '/'):
                    file_name = file_name[1:]
                file_name = file_name[l:]
            else:
                repos = rm.get_repository('')
        rev = kwargs.get('rev', None)

        if kwargs.has_key('header'):
            header = kwargs.get('header')   # user specified header
        else:
            header = tag.a(file_name, href=href.browser(orig_file_name, rev=rev))
        if not header:
            header = u'\xa0'    # default value from trac.mimeview.api.py

        # TODO - 'content' is default from mimeview.api.py, but it picks
        # up text-align: center, which probably isn't the best thing if
        # we are adding a file name in the header. There isn't an obvious
        # replacement in the delivered CSS to pick over this for now though
        header_class = kwargs.get('header_class', 'content')

        src = repos.get_node(file_name, rev).get_content().read()

        context = formatter.context
        # put these into context object so annotator sees them
        context.file_name = file_name
        context.rev = rev
        context.startline = 1

        # we generally include line numbers in the output, unless it has been
        # explicitly requested otherwise. 0, no, false, none will suppress
        line_numbers = kwargs.get('line_numbers', None)
        if line_numbers is None:
            line_numbers = True
        else:
            try:
                line_numbers = int(line_numbers)
            except:
                negatory = ('no', 'false', 'none')
                line_numbers = str(line_numbers).lower() not in negatory

        # lines added up front to "trick" renderer when rendering partial
        render_prepend = []

        start, end = kwargs.get('start', None), kwargs.get('end', None)
        if start or end:
            src, start, end = self._handle_partial(src, start, end)
            context.startline = start

            if start > 2 and file_name.endswith('.php'):
                render_prepend = [ '#!/usr/bin/php -f', '<?' ]

            if render_prepend:
                src = '\n'.join(render_prepend) + '\n' + src

                # ensure accurate start number after this gets stripped
                context.startline = start - len(render_prepend)
        else:
            start = 1

        mimetype = kwargs.get('mimetype', None)
        url = None  # render method doesn't seem to use this

        mv = Mimeview(self.env)
        annotations = line_numbers and ['lineno'] or None

        formatter.context.set_hints(lineno=start)
        src = mv.render(formatter.context, mimetype, src, file_name, url, annotations)

        if line_numbers:
            src = XML(src)

            # the _render_source method will always set the CSS class
            # of the annotator to it's name; there isn't an easy way
            # to override that. We could create our own CSS class for
            # givenlineno that mimics lineno, but it's cleaner to just
            # tweak the output here by running the genshi stream from
            # src through a transformer that will make the change

            xpath1 = 'thead/tr/th[@class="givenlineno"]'
            xpath2 = 'thead/tr/th[2]'   # last() not supported by Genshi?
            xpath3 = 'thead/tr/th[2]/text()'

            # TODO - does genshi require a QName here? Seems to work w/o it
            src = src | Transformer(xpath1).attr('class', 'lineno') \
                      | Transformer(xpath2).attr('class', header_class) \
                      | Transformer(xpath3).replace(header)
            return src

            if render_prepend:
                # TODO - is there a better of stripping lines here?
                for i in xrange(len(render_prepend)):
                    src = src | Transformer('tbody/tr[1]').remove()

        return src

    def _handle_partial(self, src, start, end):
        # we want to only show a certain number of lines, so we
        # break the source into lines and set our numbers for 1-based
        # line numbering.
        #
        # Note that there are some good performance enhancements that
        # could be done by
        # a) reading lines out of Subversion, using svn_stream_readline
        #    instead of svn_stream_read when fetching data
        # b) have the render method accept a list/iterator of lines
        #    instead of only accepting a string (which it then splits)
        lines = src.split('\n')
        linecount = len(lines)

        if start:
            start = int(start)
            if start >= 0:
                start -= 1
        if end:
            end = int(end)
        src = lines[start:end]

        # calculate actual startline for display purposes
        if not start:
            start = 1
        elif start < 0:
            start = linecount + start + 1
        else:
            start += 1

        return '\n'.join(src), start, end
