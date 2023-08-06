#=========================#
#       SVG library       #
#   Author: S-3-14-2020   #
#=========================#
class path():
	''' This base class stores SVG paths
	'''
	def __init__(self,coords=[],controls=[],drawF="QUADRATIC", **kwargs):	#**kwargs should be used here but idk how yet
		'''
		XXX parameters supplied are passed with underscores in place of dashses, and replaced before written to file
		Args:
			drawF (method): method to draw path - defaults to quadratic, o/w string literal of function
		Raises:
			ValueError: drawF argument not recognized
		'''
		self.coords=coords
		self.controls=controls
		draw_functions={
			None:self.quadratic,
			"PATH":self.path,
			"POLYLINE":self.polyline,
			"POLYGON":self.polygon,
			"QUADRATIC":self.quadratic,
			"USE":self.use
			}
		drawF=drawF.upper()
		if drawF in draw_functions:
			self.draw=draw_functions[drawF]	# could also simply assign __str__ these methods
		else:
			raise ValueError
		# css
		self.parameters={ # any parameters that are None are not written
			"stroke":"black",
			"fill":"transparent",
			"fill_opacity":0,
			"stroke_width":5
			}
		self.parameters.update(kwargs)

	@property
	def write_parameters(self):
		string=""
		for k,v in self.parameters.items():
			if not isinstance(k,str):
				raise TypeError(f"path.parameters keys must be strings, not '{type(k)}'")
			if v is not None:
				string+=f'{k.replace("_","-")}="{str(v)}" ' # replace all underscores with dashes
		return string[:-1] # not last char

	def path(self):
		first=True
		string='<path d="'
		for x,y in self.coords:
			if first:
				string+=f'M {x} {y} '
				first=False
				continue
			string+=f'L {x} {y} '
		string+=f'" {self.write_parameters}/>\n'
		return string


	def __repr__(self):
		parameters=str(self.parameters).replace(', ','\n').replace(' ','\t')[1:-1]
		return (
			f"Type: 	{self.draw.__name__}\n"
			f"Coords:	{self.coords}\n"
			f"Controls:	{self.controls}\n"
			f"{parameters}"	# isn't inline b/c f-strings dont allow backslashes? -_-
			)
	def __str__(self):
		return self.draw()


	def polyline(self):
		'''outputs a string of path represented as a polyline
		'''
		string='<polyline points="'
		for x,y in self.coords:
			string+=f"{x},{y} "
		string=string[:-1]	#cut out last space
		string+=f'" {self.write_parameters}/>\n'
		return string
	def polygon(self):
		'''outputs string of points as a polygon
		probably could simplify polyline and polygon into wrappers or a single function
		'''
		string='<polygon points="'
		for x,y in self.coords:
			string+=f"{x},{y} "
		string=string[:-1]	#cut out last space
		string+=f'" {self.write_parameters}/>\n'
		return string
	def quadratic(self):
		if len(self.coords)<2:	# need at least a start and end point
			return None
		if len(self.controls)==len(self.coords)-1:	# control for each
			# <path d="M 10 80 Q 95 10 180 80" stroke="black" fill="transparent"/>
			x,y=self.coords[0]
			string=f'<path d="M {x0} {y0} '
			for coord,control in zip(self.coords[1:],self.controls):	# may or may not be other points
				x,y=coord
				cx,cy=control
				string+=f"Q {cx} {cy}, {x} {y} "
			string=string[:-1]	# chop off trailing space
			string+=f'" {self.write_parameters}/>\n'
		elif len(self.controls)>=1:	# smooth curves
			# <path d="M 10 80 Q 52.5 10, 95 80 T 180 80" stroke="black" fill="transparent"/>
			x0,y0=self.coords[0]
			cx,cy=self.controls[0]
			x1,y1=self.coords[1]
			string=f'<path d="M {x0} {y0} Q {cx} {cy}, {x1} {y1} '
			for x,y in self.coords[2:]:	# may or may not be other points
				string+=f"T {x} {y} "
			string=string[:-1]	# chop off trailing space
			string+=f'" {self.write_parameters}/>\n'
		else:
			string=self.polyline()	# no control points - can also return path with L's
		return string

	def use(self):
		'''<use xlink:href="#house"
		x="0" y="0"
		transform="rotate(100 83 26)"/>
		'''
		try:
			uid=self.parameters["id"]
			transform=self.parameters["transform"]
		except:
			raise LookupError("'id' or 'transform' missing from path.parameters")
		if "x" in self.parameters:
			x=self.parameters["x"]
		if "y" in self.parameters:
			y=self.parameters["y"]
		return f'<use xlink:href="#{uid}" x="{x}" y="{y}" transform="{transform}"/>\n'

	def circle(self):
		pass
	def ellipse(self):
		pass
#===================================================================================================
class file():
	''' This base class stores, manipulates, and outputs path objects to SVG files
	'''
	# string constants
	#__color = ("red", "orange", "yellow", "green", "blue", "purple", "red", "orange", "yellow", "green", "blue", "purple")	#for coloring
	
	def __init__(self,filename="out.svg", height=2048, width=None):
		'''
		Args:
			filename (string): Path to file to write
			height (uint): Height of svg in pixels
			width (uint): Width of svg in pixels (if omitted, defaults to height)
		'''
		self.paths=[]			# list of path objects
		self.filename=filename
		self.height=height
		if width==None:
			self.width=self.height
		else:
			self.width=width
		self._uid=0

	@property
	def center(self):
		return (self.width/2, self.height/2)
	@property
	def header(self):
		return f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
	@property
	def footer(self):
		return '</svg>'
	@property
	def uid(self):
		self._uid+=1
		return self._uid-1
	
	def __enter__(self):
		# XXX verify that file can be opened?
		return self#.paths
	def __exit__(self, type, value, traceback):
		self.write()

	def write(self):
		''' Writes all paths to file
		'''
		with open(self.filename,'w') as file:
			file.write(str(self))

	def add_path_gen(self,generator,**kwargs):
		self.paths.append(path(list(generator), **kwargs))
	def add_path(self,path):
		self.paths.append(path)
	def add_use(self,**kwargs):
		'''piggybacks on another path
		'''
		self.add_path(path(drawF="USE",**kwargs))
				
	def __str__(self):
		string = self.header
		for p in self.paths:
			string += '\t' + p.draw()
		string += self.footer
		return string
	__repr__=__str__


	def rot_arrange(self, generator,  n, origin=None):
		'''Arranges n paths around the origin with equal spacing
		'''
		if origin is None:
			origin=self.center
		ox,oy=origin
		gen_list=list(generator)	# XXX this is rather hacky, we should probably ask for a list rather than a gen, but gens are conveinent.
		for i in range(n):
			self.add_path_gen(gen_list, transform=f"rotate({360*i/n},{ox},{oy})")

	def rot_arrange_use(self, generator,  n, origin=None):
		'''Uses a base path and references that path to save filespace
		'''
		if origin is None:
			origin=self.center
		ox,oy=origin
		uid=self.uid
		self.add_path_gen(generator,id=uid)
		for i in range(1,n):
			self.add_use(id=uid, x=0, y=0, transform=f"rotate({360*i/n},{ox},{oy})")