import spidev


class ST7920:
	def __init__(self):
		self.spi = spidev.SpiDev()
		self.spi.open(0, 0)
		self.spi.max_speed_hz = 1800000  # Set SPI clock to 1.8MHz
		
		self.send(0, 0, 0x30)  # Function set: basic instruction
		self.send(0, 0, 0x30)  # Repeat -> Function set: basic instruction
		self.send(0, 0, 0x0C)  # Display Control: display on & cursor off & blink off
		
		self.send(0, 0, 0x34)  # Extended function set: extended instruction
		self.send(0, 0, 0x34)  # Repeat -> Extended function set: extended instruction
		self.send(0, 0, 0x36)  # Extended function set: extended instruction & enable graphics display
	
	def send(self, rs, rw, cmds):
		if type(cmds) is int:  # If a single arg, convert to a list
			cmds = [cmds]
		b1 = 0b11111000 | ((rw & 0x01) << 2) | ((rs & 0x01) << 1)
		bytes = []
		for cmd in cmds:
			bytes.append(cmd & 0xF0)
			bytes.append((cmd & 0x0F) << 4)
		return self.spi.xfer2([b1] + bytes)

	def display_control(self, display, cursor, blink):
		cmd = 0x08
		cmd = cmd | (display & 0x01) << 2
		cmd = cmd | (cursor & 0x01) << 1
		cmd = cmd | blink
		self.send(0, 0, cmd)
		print("display_control " + str(cmd))

	def write_gdram(self, vadd, hadd, first, second):
		cmds = []
		cmds.append(0x80 | vadd)
		cmds.append(0x80 | hadd)
		cmds.append(first)
		cmds.append(second)

		self.send(0, 0, cmds)
		print("write_gdram " + str(cmds))
