from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

class GIF_Plasmoid( plasmascript.Applet ):
	txt = QtGui.QStaticText( "Drop GIF here!" )
	newGIF = True
	movie = None

	def __init__( self, parent, args = None ):
		plasmascript.Applet.__init__( self, parent )

	def init( self ):
		self.setHasConfigurationInterface( False )
		self.setAcceptDrops( True )
		args = self.startupArguments()
		if args:
			self.loadGIF( self.startupArguments()[ 0 ].toUrl().toLocalFile().toLocal8Bit().data(), True )
		else:
			self.loadGIF( self.config().readEntry( "URL" ), False );

	def loadGIF( self, url, save ):
		tmp_movie = QtGui.QMovie( self )
		tmp_movie.setCacheMode( QtGui.QMovie.CacheAll )
		tmp_movie.setFileName( url )
		if tmp_movie.format() == "gif":
			if save:
				self.config().writeEntry( "URL", url )
			self.movie = tmp_movie
			self.movie.updated.connect( self.update )
			self.newGIF = True
			self.movie.start()

	def paintInterface( self, painter, option, rect ):
		widgetSize = self.size().toSize()
		deltaSize = widgetSize - rect.size()
		if self.movie:
			if self.newGIF or self.movie.frameRect().size() + deltaSize == widgetSize:
				gifFrame = self.movie.currentPixmap()
			else:
				gifFrame = self.movie.currentPixmap().scaled( rect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation )
			self.newGIF = False
			painter.drawPixmap( rect.x(), rect.y(), gifFrame )
			s = QtCore.QSizeF( gifFrame.size() + deltaSize )
			self.setMinimumSize( deltaSize.width() * 1.5, deltaSize.height() * 1.5 )
			self.setMaximumSize( 16777215.0, 16777215.0 )
			if widgetSize != s:
				self.resize( s )
		else:
			s = QtCore.QSizeF( self.txt.size().toSize() + deltaSize )
			self.setMinimumSize( s )
			self.setMaximumSize( s )
			painter.drawStaticText( rect.x(), rect.y(), self.txt )

	def dragEnterEvent( self, e ):
		if e.mimeData().hasUrls():
			e.accept()
		else:
			e.ignore()

	def dropEvent( self, e ):
		self.loadGIF( e.mimeData().urls()[ 0 ].toLocalFile().toLocal8Bit().data(), True )

def CreateApplet( parent ):
	return GIF_Plasmoid( parent )
