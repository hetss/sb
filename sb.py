import re
import MySQLdb
import logging
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()

# TODO:
#

class exhibHandler:
	red_id = 0
	blue_id = 0
	def __init__(self,redname,bluename):
		self.db = MySQLdb.connect(host="10.0.0.3",
								  user="gustav",
								  passwd="kalleanka",
								  db="saltybet")
		self.c = self.db.cursor()
		self.redname = redname
		self.bluename = bluename

		self.c.execute("SELECT * FROM fighter WHERE name = %s", [self.redname])
		if(self.c.rowcount == 0):
			self.red_id = 0
		else:
			temp = self.c.fetchone()
			self.red_id = temp[0]
		self.c.execute("SELECT * FROM fighter WHERE name = %s", [self.bluename])
		if(self.c.rowcount == 0):
			self.blue_id = 0
		else:
			temp = self.c.fetchone()
			self.blue_id = temp[0]
		if(self.blue_id != 0 or self.red_id != 0):
			try:
				self.c.execute("UPDATE active_match SET fighter1 = %s, fighter2 = %s WHERE id = 1",(self.red_id,self.blue_id))
				self.db.commit()
			except:
				print "Active match update failed!"
				self.db.rollback()
		print "\r\nFight:\t"+self.redname+" vs. "+self.bluename+" (Exhibition)"


class matchHandler:
	redbet = None
	redstats = None
	bluebet = None
	bluestats = None
	red_id = 0
	blue_id = 0
	red_promo = False
	red_demote = False
	blue_promo = False
	blue_demote = False

	def promote(self,f,t):
		if(t.upper() == 'A' or t.upper() == 'B'):
			try:
				self.c.execute("INSERT INTO `event` (fighter,description) VALUES (%s,%s)",(f,'Promoted from '+t))
				self.db.commit()
				return True
			except:
				print "Promotion insert failed"
				self.db.rollback()
		return False

	def demote(self,f,t):
		if(t.upper() == 'S' or t.upper() == 'A' or t.upper() == 'B'):
			try:
				self.c.execute("INSERT INTO `event` (fighter,description) VALUES (%s,%s)",(f,'Demoted from '+t))
				self.db.commit()
				return True
			except:
				print "Demotion insert failed"
				self.db.rollback()
		return False

	def __init__(self,redname,bluename,tier,tournament=False):
		self.db = MySQLdb.connect(host="10.0.0.3",
								  user="gustav",
								  passwd="kalleanka",
								  db="saltybet")
		self.c = self.db.cursor()
		self.redname = redname
		self.bluename = bluename
		if(self.redname == "Chili n ***"):
			self.redname = "Chili n pepper"
		if(self.bluename == "Chili n ***"):
			self.bluename = "Chili n pepper"
		self.tier = tier
		self.bet = False
		self.lock = False

		self.c.execute("SELECT * FROM fighter WHERE name = %s", [self.redname])
		if(self.c.rowcount == 0):
			try:
				self.c.execute("INSERT INTO fighter (name,tier,stats) VALUES (%s,%s,%s)", (self.redname, self.tier, 0))
				self.db.commit()
			except:
				print "Fighter 1 insert failed!"
				self.db.rollback()
			self.red_id = self.c.lastrowid
		else:
			temp = self.c.fetchone()
			self.red_id = temp[0]
		self.c.execute("SELECT * FROM fighter WHERE name = %s", [self.bluename])
		if(self.c.rowcount == 0):
			try:
				self.c.execute("INSERT INTO fighter (name,tier,stats) VALUES (%s,%s,%s)", (self.bluename, self.tier, 0))
				self.db.commit()
			except:
				print "Fighter 2 insert failed!"
				self.db.rollback()
			self.blue_id = self.c.lastrowid
		else:
			temp = self.c.fetchone()
			self.blue_id = temp[0]

		try:
			if(tournament):
				self.c.execute("UPDATE active_match SET fighter1 = %s, fighter2 = %s, tournament = 1, open=NOW() WHERE id = 1",(self.red_id,self.blue_id))
			else:
				self.c.execute("UPDATE active_match SET fighter1 = %s, fighter2 = %s, tournament = 0, open=NOW() WHERE id = 1",(self.red_id,self.blue_id))
			self.db.commit()
		except:
			print "Active match update failed!"
			self.db.rollback()

		print "\r\nFight:\t"+Fore.RED+self.redname+Style.RESET_ALL+" vs. "+Fore.CYAN+self.bluename+Style.RESET_ALL+" ("+self.tier+" Tier)"

	def enablePromo(self, fighter):
		if(fighter == self.redname):
			self.red_promo = True
			print "\tPromo match for"+fighter+" (red)"
		if(fighter == self.bluename):
			self.blue_promo = True
			print "\tPromo match for"+fighter+" (blue)"

	def enableDemote(self, fighter):
		if(fighter == self.redname):
			self.red_demote = True
			print "\tDemotion match for"+fighter+" (red)"
		if(fighter == self.bluename):
			self.blue_demote = True
			print "\tDemotion match for"+fighter+" (blue)"

	def confirmPromo(self, fighter):
		if(fighter == self.redname and self.red_promo):
			if(self.promote(self.red_id,self.tier)):
				new_redstats = 0
				self.red_promo = False
				try:
					self.c.execute("UPDATE fighter SET stats = %s WHERE id = %s",(new_redstats,self.red_id))
					self.db.commit()
					print "\t"+self.redname+" was promoted."
				except:
					print "Promotion update failed!"
					self.db.rollback()
		if(fighter == self.bluename and self.blue_promo):
			if(self.promote(self.blue_id,self.tier)):
				new_bluestats = 0
				self.blue_promo = False
				try:
					self.c.execute("UPDATE fighter SET stats = %s WHERE id = %s",(new_bluestats,self.blue_id))
					self.db.commit()
					print "\t"+self.bluename+" was promoted."
				except:
					print "Promotion update failed!"
					self.db.rollback()

	def confirmDemote(self, fighter):
		if(fighter == self.redname and self.red_demote):
			if(self.demote(self.red_id,self.tier)):
				new_redstats = 0
				self.red_demote = False
				try:
					self.c.execute("UPDATE fighter SET stats = %s WHERE id = %s",(new_redstats,self.red_id))
					self.db.commit()
					print "\t"+self.redname+" was demoted."
				except:
					print "Demotion update failed!"
					self.db.rollback()
		if(fighter == self.bluename and self.blue_demote):
			if(self.demote(self.blue_id,self.tier)):
				new_bluestats = 0
				self.blue_demote = False
				try:
					self.c.execute("UPDATE fighter SET stats = %s WHERE id = %s",(new_bluestats,self.blue_id))
					self.db.commit()
					print "\t"+self.bluename+" was demoted."
				except:
					print "Demotion update failed!"
					self.db.rollback()
		
	def applyBet(self,redbet,bluebet,redstats,bluestats):
		if(not self.lock and not self.bet):
			self.redbet = int(redbet)
			self.redstats = int(redstats)
			self.bluebet = int(bluebet)
			self.bluestats = int(bluestats)
			self.bet = True
			if(self.red_id != 0 and self.blue_id != 0):
				try:
					self.c.execute("UPDATE fighter SET stats = %s WHERE id = %s",(self.redstats,self.red_id))
					self.c.execute("UPDATE fighter SET stats = %s WHERE id = %s",(self.bluestats,self.blue_id))
					self.c.execute("UPDATE active_match SET modified=NOW() WHERE id = 1")
					self.db.commit()
				except:
					print "Fighter update failed!"
					self.db.rollback()

			print "\t$"+str(self.redbet)+" ("+str(self.redstats)+") | $"+str(self.bluebet)+" ("+str(self.bluestats)+")"

	def win(self,team,name):
		if(name == "Chili n ***"):
			name = "Chili n pepper"
		if(self.bet and not self.lock):
			self.lock = True
			self.c.execute("SELECT * FROM fighter WHERE name = %s", [self.redname])
			if(self.c.rowcount == 0):
				try:
					self.c.execute("INSERT INTO fighter (name,tier,stats) VALUES (%s,%s,%s)", (self.redname, self.tier, self.redstats))
					self.db.commit()
				except:
					print "Fighter 1 insert failed!"
					self.db.rollback()
				self.red_id = self.c.lastrowid
			else:
				temp = self.c.fetchone()
				self.red_id = temp[0]
			self.c.execute("SELECT * FROM fighter WHERE name = %s", [self.bluename])
			if(self.c.rowcount == 0):
				try:
					self.c.execute("INSERT INTO fighter (name,tier,stats) VALUES (%s,%s,%s)", (self.bluename, self.tier, self.bluestats))
					self.db.commit()
				except:
					print "Fighter 2 insert failed!"
					self.db.rollback()
				self.blue_id = self.c.lastrowid
			else:
				temp = self.c.fetchone()
				self.blue_id = temp[0]

			if(team.lower() == 'red'):
				print "\t"+self.redname+" won ("+Fore.RED+"red"+Style.RESET_ALL+")"
				if(self.redname == name):
					winner = self.red_id
					if(self.redstats<0):
						new_redstats = 1
					else:
						new_redstats = self.redstats+1
						if(self.red_promo):
							if(self.promote(self.red_id,self.tier)):
								new_redstats = 0
								self.red_promo = False
					if(self.bluestats<0):
						new_bluestats = self.bluestats-1
						if(self.blue_demote):
							if(self.demote(self.blue_id,self.tier)):
								new_bluestats = 0
								self.blue_demote = False
					else:
						new_bluestats = -1
				else:
					print "Name discrepancy detected! Aborting"
					return
			elif(team.lower() == 'blue'):
				print "\t"+self.bluename+" won ("+Fore.CYAN+"blue"+Style.RESET_ALL+")"
				if(self.bluename == name):
					winner = self.blue_id
					if(self.redstats<0):
						new_redstats = self.redstats-1
						if(self.red_demote):
							if(self.demote(self.red_id,self.tier)):
								new_redstats = 0
								self.red_demote = False
					else:
						new_redstats = -1
					if(self.bluestats<0):
						new_bluestats = 1
					else:
						new_bluestats = self.bluestats+1
						if(self.blue_promo):
							if(self.promote(self.blue_id,self.tier)):
								new_bluestats = 0
								self.blue_promo = False
				else:
					print "Name discrepancy detected! Aborting"
					return
			try:
				if(team.lower() == 'red'):
					self.c.execute("UPDATE fighter SET stats = %s, fights = fights+1, wins = wins+1, tier = %s WHERE id = %s",(new_redstats,self.tier,self.red_id))
					self.c.execute("UPDATE fighter SET stats = %s, fights = fights+1, losses = losses+1, tier = %s WHERE id = %s",(new_bluestats,self.tier,self.blue_id))
				else:
					self.c.execute("UPDATE fighter SET stats = %s, fights = fights+1, wins = wins+1, tier = %s WHERE id = %s",(new_bluestats,self.tier,self.blue_id))
					self.c.execute("UPDATE fighter SET stats = %s, fights = fights+1, losses = losses+1, tier = %s WHERE id = %s",(new_redstats,self.tier,self.red_id))
				
				self.c.execute("INSERT INTO `match` (fighter1,fighter2,bet1,bet2,winner) VALUES (%s,%s,%s,%s,%s)", (self.red_id,self.blue_id,self.redbet,self.bluebet,winner))
				self.db.commit()
			except:
				print "Match insert failed"
				self.db.rollback()

	def __del__(self):
		self.c.close()
		self.db.close()

class saltyBet:
	mm_betsopen = r"Bets are OPEN for (?P<name1>.*) vs (?P<name2>.*)! \((?P<tier>[A-z]{1}) Tier\) \(matchmaking\)"
	mm_new_betsopen = r"Bets are OPEN for (?P<name1>.*) vs (?P<name2>.*)! \(NEW Tier\) \(matchmaking\)"
	mm_betslocked = r"Bets are locked\. (?P<name1>.*) \((?P<stats1>[-]?\d+)\) - \$(?P<bet1>\d+(?:\,+\d{3})*), (?P<name2>.*) \((?P<stats2>[-]?\d+)\) - \$(?P<bet2>\d+(?:\,+\d{3})*)"
	tourney_betsopen = r"Bets are OPEN for (?P<name1>.*) vs (?P<name2>.*)! \((?P<tier>[A-z]{1}) Tier\) tournament bracket"
	exhib_betsopen = r"Bets are OPEN for (?P<name1>.*) vs (?P<name2>.*)! (\((?P<tier>[A-z]{1}) Tier\) )?\(.*\) \(exhibitions\)"
	exhib_betslocked = r"Bets are locked\. (?P<name1>.*)- \$(?P<bet1>\d+(?:\,+\d{3})*), (?P<name2>.*)- \$(?P<bet2>\d+(?:\,+\d{3})*)"
	regexp_tier = r"(?P<tier>[A-z]{1})( / (?P<tier2>[A-z]{1}))? Tier$"
	regexp_win = r"(?P<name>.*) wins! Payouts to Team (?P<team>.*)\."

	promo_start = r"ACTION wtfSALTY (?P<promoname>.*) is fighting for a promotion from (?P<curtier>.{1}) to (?P<promotier>.{1}) Tier!"
	promo_confirm = r"ACTION wtfSALTY (?P<promoname>.*) has been promoted!"
	demote_start = r"ACTION wtfSALTY (?P<demotename>.*) is fighting to stay in (?P<curtier>.{1}) Tier!"
	demote_confirm = r"ACTION wtfSALTY (?P<demotename>.*) has been demoted!"

	match = None

	def __init__(self):
		self.match = None

		self.logger = logging.getLogger('saltybet')
		handler = logging.FileHandler('saltybet.log')
		formatter = logging.Formatter('%(asctime)s: %(message)s')
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)
		self.logger.setLevel(logging.INFO)

	def parse(self,msg):
		#print "\t("+msg.encode("utf-8")+")"
		self.logger.info(msg.encode("utf-8"))
		r = re.match(self.mm_betsopen,msg) # Matchmaking bet open
		if(r != None):
			name1 = r.group('name1')
			name2 = r.group('name2')
			tier = r.group('tier')
			self.match = matchHandler(name1,name2,tier)
			return
		r = re.match(self.mm_new_betsopen,msg) # Matchmaking (NEW Tier) bet open
		if(r != None):
			name1 = r.group('name1')
			name2 = r.group('name2')
			tier = 'N'
			self.match = matchHandler(name1,name2,tier)
			return
		r = re.match(self.tourney_betsopen,msg) # Tourney bet open
		if(r != None):
			name1 = r.group('name1')
			name2 = r.group('name2')
			tier = r.group('tier')
			self.match = matchHandler(name1,name2,tier,True)
			return
		r = re.match(self.mm_betslocked,msg) # Matchmaking/tourney bet lock
		if(r != None and self.match != None):
			name1 = r.group('name1')
			stats1 = r.group('stats1')
			bet1 = r.group('bet1').replace(',','')
			name2 = r.group('name2')
			stats2 = r.group('stats2')
			bet2 = r.group('bet2').replace(',','')
			self.match.applyBet(bet1,bet2,stats1,stats2)
			return
		r = re.match(self.regexp_win,msg) # Win
		if(r != None and self.match != None):
			name = r.group('name')
			team = r.group('team')
			self.match.win(team,name)
			return
		r = re.match(self.exhib_betslocked,msg) # Exhib/P-tier bet lock
		if(r != None and self.match != None):
			name1 = r.group('name1')
			bet1 = r.group('bet1').replace(',','')
			name2 = r.group('name2')
			bet2 = r.group('bet2').replace(',','')
			self.match.applyBet(bet1,bet2,0,0)
			return
		r = re.match(self.exhib_betsopen,msg) # Exhib bet open
		if(r != None):
			name1 = r.group('name1')
			name2 = r.group('name2')
			temp = exhibHandler(name1,name2)
			return
		r = re.match(self.promo_start, msg) # Enable promotion for fighter
		if(r != None):
			name = r.group('promoname')
			self.match.enablePromo(name)
			return
		r = re.match(self.demote_start, msg) # Enable demotion for fighter
		if(r != None):
			name = r.group('demotename')
			self.match.enableDemote(name)
			return
		r = re.match(self.promo_confirm, msg) # Confirm promotion for fighter
		if(r != None):
			name = r.group('promoname')
			if(self.match != None):
				self.match.confirmPromo(name)
			return
		r = re.match(self.demote_confirm, msg) # Confirm demotion for fighter
		if(r != None):
			name = r.group('demotename')
			if(self.match != None):
				self.match.confirmDemote(name)
			return
		#r = re.match(self.regexp_tier,msg) # Tier message
		#if(r != None):
		#	current_tier = r.group('tier')
		#	current_tier2 = r.group('tier2')
		#	if(current_tier2 != None):
		#		print "Current tiers: "+current_tier+" / "+current_tier2
		#		return
		#	print "Current tier: "+current_tier
		#	return