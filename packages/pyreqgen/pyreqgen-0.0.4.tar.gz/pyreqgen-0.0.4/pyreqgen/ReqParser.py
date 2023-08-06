#!/usr/bin/env python3
import os, sys

class ReqParser(object):

	@staticmethod
	def __check_py(file_s: str):
		"""
		check to see if a file is a python file
		:return: boolean: whether the file is a python file or not
		"""
		if type(file_s) is not str:
			raise Exception("file name must be a string")
		return file_s.endswith("py")

	@staticmethod
	def __get_py_files(src_dir_s : str):
		if type(src_dir_s) is str:
			src_dir_d = os.walk(src_dir_s)
			file_set = set()
			for r, d_s, f_s in src_dir_d:
				for f in f_s:
					if ReqParser.__check_py(f):
						file_set.add(os.path.join(r, f))
		else:
			raise Exception("source directory file path needs to be a string")
		return file_set

	@staticmethod
	def __parse_package(p_l):
		if len(p_l) == 1:
			return None

		if '.' in p_l:
			wo_dot_p = p_l.split(".")[0]
			if wo_dot_p not in sys.modules:
				return wo_dot_p
			return None

		if p_l not in sys.modules:
			return p_l
		else:
			return None
		return p_l

	@staticmethod
	def __parse_line(l):
		"""
		parses a line of text for the package to install
		"""
		s_l = l.split()

		if len(s_l) < 2:
			return None
		if any(x in s_l[0] for x in ("from", "import")):
			return ReqParser.__parse_package(s_l[1])
		else:
			return None

	@staticmethod
	def __parse_file(f_s, reqs):

		with open(f_s, "r+") as f:
			lines = f.readlines()
			for l in lines:
				req = ReqParser.__parse_line(l)
				if req is not None:
					reqs.add(req)
		return reqs

	@staticmethod
	def __get_reqs(py_files):
		reqs = set()

		while (len(py_files) > 0):
			f = py_files.pop()
			reqs = ReqParser.__parse_file(f, reqs)

		return reqs

	@staticmethod
	def run(src_dir_s, write_o=False, alpha=False):
		py_files = ReqParser.__get_py_files(src_dir_s)
		reqs = ReqParser.__get_reqs(py_files)
		if write_o:
			ReqParser.write(reqs, alpha)
		else:
			return reqs

	@staticmethod
	def write(req_set, alpha=False):
		reqs = list(req_set)

		# soft if the option is set
		if alpha:
			reqs.sort()

		# TODO: write to the folder of your choosing
		with open("requirements.txt", 'w+') as req_f:
			req_f.write('\n'.join(reqs))