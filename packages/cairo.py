class CairoPackage (CairoGraphicsXzPackage):
	def __init__ (self):
		CairoGraphicsXzPackage.__init__ (self, 'cairo', '1.12.14')
		self.sources.extend ([
			'patches/cairo-quartz-crash.patch',
			'patches/cairo-fix-color-bitmap-fonts.patch',
#			'patches/cairo-cglayer.patch',
		])
		#This package would like to be built with fat binaries
		if Package.profile.m64 == True:
			self.fat_build = True

	def prep (self):
		Package.prep (self)

		if Package.profile.name == 'darwin':
			for p in range (1, len (self.sources)):
				self.sh ('patch -p1 < "%{sources[' + str (p) + ']}"')

	def build (self):
		self.configure_flags = [
			'--enable-pdf',
			'--enable-debug'
		]

		if Package.profile.name == 'darwin':
			self.configure_flags.extend ([
				'--enable-quartz',
				'--enable-quartz-font',
				'--enable-quartz-image',
				'--disable-xlib',
				'--without-x'
			])
		elif Package.profile.name == 'linux':
			self.configure_flags.extend ([
				'--disable-quartz',
				'--with-x'
			])

		Package.build (self)

CairoPackage ()
