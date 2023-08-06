import os
import re

from collections import OrderedDict
from urllib.parse import unquote, urlsplit, urlunsplit

from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.contrib.staticfiles.utils import matches_patterns
from django.core.files.base import ContentFile

class FlexibleManifestStaticFilesStorage(ManifestStaticFilesStorage):

    whitelisted_patterns = getattr(settings, "STATICFILES_VERSIONED_INCLUDE", ['.*'])
    blacklisted_patterns = getattr(settings, "STATICFILES_VERSIONED_EXCLUDE", [])

    # def save_manifest(self):

    #     filtered_hashed_files = OrderedDict()

    #     for original_url, hashed_url in self.hashed_files.items():

    #         should_convert = False
    #         if any(re.search(wp, original_url) for wp in self.whitelisted_patterns):
    #             if not any(re.search(bp, original_url) for bp in self.blacklisted_patterns):
    #                 should_convert = True
            
    #         if should_convert:
    #             filtered_hashed_files[original_url] = hashed_url
    #         else:
    #             filtered_hashed_files[original_url] = original_url

    #     self.hashed_files = filtered_hashed_files

    #     return super().save_manifest()

    def hashed_name(self, name, content=None, filename=None):

        if any(re.search(wp, name) for wp in self.whitelisted_patterns):
            if not any(re.search(bp, name) for bp in self.blacklisted_patterns):

                return super().hashed_name(name, content, filename)

        return name

        # `filename` is the name of file to hash if `content` isn't given.
        # `name` is the base name to construct the new hashed filename from.
        # parsed_name = urlsplit(unquote(name))
        # clean_name = parsed_name.path.strip()
        # filename = (filename and urlsplit(unquote(filename)).path.strip()) or clean_name
        # opened = content is None
        # if opened:
        #     if not self.exists(filename):
        #         raise ValueError("The file '%s' could not be found with %r." % (filename, self))
        #     try:
        #         content = self.open(filename)
        #     except IOError:
        #         # Handle directory paths and fragments
        #         return name
        # try:
        #     file_hash = self.file_hash(clean_name, content)
        # finally:
        #     if opened:
        #         content.close()
        # path, filename = os.path.split(clean_name)
        # root, ext = os.path.splitext(filename)
        # if file_hash is not None:
        #     file_hash = ".%s" % file_hash

        # should_convert = False
        # if any(re.search(wp, filename) for wp in self.whitelisted_patterns):
        #     if not any(re.search(bp, filename) for bp in self.blacklisted_patterns):
        #         should_convert = True
        
        # if should_convert:
        #     hashed_name = os.path.join(path, "%s%s%s" %
        #                            (root, file_hash, ext))
        # else:
        #     hashed_name = name

        # unparsed_name = list(parsed_name)
        # unparsed_name[2] = hashed_name
        # # Special casing for a @font-face hack, like url(myfont.eot?#iefix")
        # # http://www.fontspring.com/blog/the-new-bulletproof-font-face-syntax
        # if '?#' in name and not unparsed_name[3]:
        #     unparsed_name[2] += '?'

        # print("name")
        # print(name)
        # print("filename")
        # print(filename)
        # print("unparsed_name")
        # print(unparsed_name)
        # print("-------")
        # return urlunsplit(unparsed_name)

    # def post_process(self, paths, dry_run=False, **options):
    #     """
    #     Post process the given OrderedDict of files (called from collectstatic).

    #     Processing is actually two separate operations:

    #     1. renaming files to include a hash of their content for cache-busting,
    #        and copying those files to the target storage.
    #     2. adjusting files which contain references to other files so they
    #        refer to the cache-busting filenames.

    #     If either of these are performed on a file, then that file is considered
    #     post-processed.
    #     """
    #     # don't even dare to process the files if we're in dry run mode
    #     if dry_run:
    #         return

    #     # where to store the new paths
    #     hashed_files = OrderedDict()

    #     # build a list of adjustable files
    #     adjustable_paths = [
    #         path for path in paths
    #         if matches_patterns(path, self._patterns)
    #     ]
    #     # Do a single pass first. Post-process all files once, then repeat for
    #     # adjustable files.
    #     for name, hashed_name, processed, _ in self._post_process(paths, adjustable_paths, hashed_files):
    #         yield name, hashed_name, processed
    #         # should_convert = False

    #         # if any(re.search(wp, name) for wp in self.whitelisted_patterns):
    #         #     if not any(re.search(bp, name) for bp in self.blacklisted_patterns):
    #         #         should_convert = True

    #         # if should_convert:
    #         #     yield name, hashed_name, processed
    #         # else:
    #         #     yield name, name, processed


    #     paths = {path: paths[path] for path in adjustable_paths}

    #     for i in range(self.max_post_process_passes):
    #         substitutions = False
    #         for name, hashed_name, processed, subst in self._post_process(paths, adjustable_paths, hashed_files):
    #             yield name, hashed_name, processed
    #             # if any(re.search(wp, name) for wp in self.whitelisted_patterns):
    #             #     if not any(re.search(bp, name) for bp in self.blacklisted_patterns):
    #             #         should_convert = True

    #             # if should_convert:
    #             #     yield name, hashed_name, processed
    #             # else:
    #             #     yield name, name, processed

    #             substitutions = substitutions or subst

    #         if not substitutions:
    #             break

    #     if substitutions:
    #         yield 'All', None, RuntimeError('Max post-process passes exceeded.')

    #     # Store the processed paths
    #     print("hashed_files")
    #     print(hashed_files)

    #     filtered_hashed_files = OrderedDict()

    #     for original_url, hashed_url in hashed_files.items():

    #         should_convert = False
    #         if any(re.search(wp, original_url) for wp in self.whitelisted_patterns):
    #             if not any(re.search(bp, original_url) for bp in self.blacklisted_patterns):
    #                 should_convert = True
            
    #         if should_convert:
    #             filtered_hashed_files[original_url] = hashed_url
    #         else:
    #             filtered_hashed_files[original_url] = original_url


    #     print("filtered_hashed_files")
    #     print(filtered_hashed_files)

    #     self.hashed_files.update(filtered_hashed_files)

    # def _post_process(self, paths, adjustable_paths, hashed_files):

    #     print("=======")
    #     print("paths:")
    #     print(paths)
    #     print("=======")
    #     print("adjustable_paths:")
    #     print(adjustable_paths)
    #     print("=======")
    #     print("hashed_files:")
    #     print(hashed_files)
    #     print("=======")
    #     filtered_paths = OrderedDict()

    #     for name, val in paths.items():
    #         if any(re.search(wp, name) for wp in self.whitelisted_patterns):
    #             if not any(re.search(bp, name) for bp in self.blacklisted_patterns):
    #                 filtered_paths[name] = val
        
    #     return super()._post_process(filtered_paths, adjustable_paths, hashed_files)

    # def _post_process(self, paths, adjustable_paths, hashed_files):

    #     filtered_hashed_files = OrderedDict()

    #     for original_url, hashed_url in hashed_files.items():

    #         should_convert = False
    #         if any(re.search(wp, original_url) for wp in self.whitelisted_patterns):
    #             if not any(re.search(bp, original_url) for bp in self.blacklisted_patterns):
    #                 should_convert = True
            
    #         if should_convert:
    #             # print("AM CONVERTING")
    #             # print(name)
    #             # print(template)
    #             # print(original_url,hashed_url)
    #             filtered_hashed_files[original_url] = hashed_url
    #         else:
    #             # print("NOT CONVERTING")
    #             # print(name)
    #             # print(template)
    #             # print(original_url,hashed_url)
    #             filtered_hashed_files[original_url] = original_url

    #     filtered_paths = OrderedDict()

    #     for name, val in paths.items():
    #         if any(re.search(wp, name) for wp in self.whitelisted_patterns):
    #             if not any(re.search(bp, name) for bp in self.blacklisted_patterns):
    #                 filtered_paths[name] = val
        
    #     return super()._post_process(filtered_paths, filtered_hashed_files, hashed_files)


    # def url_converter(self, name, hashed_files, template=None):

    #     print("=== url_converter ===")
    #     print("name")
    #     print(name)
    #     print("hashed_files")
    #     print(hashed_files)
    #     print("")
    #     print("")

    #     super_converter = super().url_converter(name, hashed_files, template)

    #     def converter(matchobj):
    #         matched, url = matchobj.groups()

    #         should_convert = False

    #         if any(re.search(wp, url) for wp in self.whitelisted_patterns):
    #             if not any(re.search(bp, url) for bp in self.blacklisted_patterns):
    #                 should_convert = True

    #         if not should_convert:
    #             print("No convert:")
    #             print(matched)
    #             return matched

    #         return super_converter(matchobj)

    #     return converter

    # def url_converter(self, name, hashed_files, template=None):

    #     filtered_hashed_files = OrderedDict()

    #     for original_url, hashed_url in hashed_files.items():

    #         should_convert = False
    #         if any(re.search(wp, original_url) for wp in self.whitelisted_patterns):
    #             if not any(re.search(bp, original_url) for bp in self.blacklisted_patterns):
    #                 should_convert = True
            
    #         if should_convert:
    #             print("AM CONVERTING")
    #             print(name)
    #             print(template)
    #             print(original_url,hashed_url)
    #             filtered_hashed_files[original_url] = hashed_url
    #         else:
    #             print("NOT CONVERTING")
    #             print(name)
    #             print(template)
    #             print(original_url,hashed_url)
    #             filtered_hashed_files[original_url] = original_url

    #     return super().url_converter(name, filtered_hashed_files, template)


    # def url_converter(self, name, hashed_files, template=None):

    #     filtered_hashed_files = OrderedDict()

    #     for original_url, hashed_url in hashed_files.items():

    #         should_convert = False
    #         if any(re.search(wp, original_url) for wp in self.whitelisted_patterns):
    #             if not any(re.search(bp, original_url) for bp in self.blacklisted_patterns):
    #                 should_convert = True
            
    #         if should_convert:
    #             # print("AM CONVERTING")
    #             # print(name)
    #             # print(template)
    #             # print(original_url,hashed_url)
    #             filtered_hashed_files[original_url] = hashed_url
    #         else:
    #             # print("NOT CONVERTING")
    #             # print(name)
    #             # print(template)
    #             # print(original_url,hashed_url)
    #             filtered_hashed_files[original_url] = original_url


    #     super_converter = super().url_converter(name, filtered_hashed_files, template)

    #     def converter(matchobj):
    #         matched, url = matchobj.groups()

    #         should_convert = False

    #         if any(re.search(wp, url) for wp in self.whitelisted_patterns):
    #             if not any(re.search(bp, url) for bp in self.blacklisted_patterns):
    #                 should_convert = True

    #         if not should_convert:
    #             return matched

    #         return super_converter(matchobj)

    #     return converter
