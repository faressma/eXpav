import sys,tty,termios
import bluetooth as bt
from msg import *

class _Getch:
	def __call__(self):
			fd = sys.stdin.fileno()
			old_settings = termios.tcgetattr(fd)
			try:
				tty.setraw(sys.stdin.fileno())
				ch = sys.stdin.read(3)
			finally:
				termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
			return ch

def get():
		inkey = _Getch()
		while(1):
			k=inkey()
			if k!='':
				break

		if k=='\x1b[A':
				print("up")
				sock.send(stop_turn()) # forward
				sock.send(forward()) # forward
		elif k=='\x1b[B':
				print("down")
				sock.send(backward()) # bakward
		elif k=='\x1b[C':
				print("right")
				sock.send(right()) # right
		elif k=='\x1b[D':
				print("left")
				sock.send(left()) # left
		elif k=='\x1bOP':
				print("F1")
				sock.send(battery_lvl())
		elif k=='\x1bOQ':
				print("F2")
				sock.send(battery_lvl())
		elif k=='\x1bOR':
				print("F3")
				sock.send(battery_lvl())
		elif k=='\x1bOS':
				print("F4")
				sock.send(battery_lvl())
		else:
				print("not an arrow key!")

def main():
		#for i in range(0,20):
		while(1) :
			get()

if __name__=='__main__':
	sock = bt.BluetoothSocket(bt.RFCOMM)
	sock.connect(('00:13:EF:D5:D3:A2',1))
	main()
