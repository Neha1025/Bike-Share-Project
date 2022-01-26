#import numpy as np
import sqlite3
from datetime import datetime

class Backend:
    def __init__(self,dbaddress="bike.db"):
        self.dbaddress=dbaddress

    # Get cities all or by ID 
    # return : 0 -> city_id, 1 -> city_name   
    def getCities(self, id=""):
        cond = ""
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
        try :
            sql = "SELECT  city_id, city_name FROM city ORDER BY city_id"
            if id != "":
                cond = "city_id = %d" % (id)
            cursor.execute( sql+ ("WHERE "+cond if cond != "" else ""))  
            return cursor.fetchall()
        except Exception as e:
            return [False, "Error : "+ str(e) ]
        finally:
             db.close()
             
    # Get Locations all or by ID or by city id
    # return : 0 -> location_id, 1 -> location_name   
    def getLocations(self, id="", city_id=""):
        cond = []
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
        try :
            sql = "SELECT  location_id, location_name, city.city_id, city_name FROM locations INNER JOIN city ON city.city_id = locations.city_id "
            if id != "":
                cond.append("location_id = %d" % (id))
            if city_id != "":
                cond.append("city.city_id = %d" % (int(city_id)))
            cursor.execute( sql+ (" WHERE "+ " AND ".join(cond) if cond != [] else "")+ " ORDER BY location_id")  
            
            return cursor.fetchall()
        except Exception as e:
            return [False, "Error : "+ str(e) ]
        finally:
             db.close()
    
    # Get Bikes all or by ID 
    # return : 0 -> bycicle_id , 1 -> location_id, 2 -> is_defective, 3 -> is_rent, 4 -> charge_rate
    #          5->  current_position_long, 6 -> current_position_lat, 7 -> is_repaired   
    def getBikes(self, id="all", loc_id="all", is_defective="all", is_rent="all",
                 is_repaired = "all"):
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
        cond = []
        try :
            sql = "SELECT  bycicle_id, location_id, is_defective, is_rent, charge_rate, current_position_long, current_position_lat, is_repaired FROM bycicle"
            if id != "all":
                cond.append( "bycicle_id = %d" % (id))
            if loc_id != "all":
                cond.append( "location_id = %d" % (loc_id))
            if is_defective != "all":
                cond.append( "is_defective = %d" % (is_defective))
            if is_rent != "all":
                cond.append( "is_rent = %d" % (is_rent))
            if is_repaired != "all":
                cond.append( "is_repaired = %d" % (is_repaired))
                
            cursor.execute( sql+ (" WHERE "+ " AND ".join(cond) if cond != [] else ""))  
            return cursor.fetchall()
        except Exception as e:
            return [False, "Error : "+ str(e) ]
        finally:
             db.close()
    
    #Insert Bike Rent 
    def AddBikeRent(self, customer_id,bycicle_id, location_start_id, start_time):
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
        sql = "INSERT INTO rent (rent_id, customer_id,bycicle_id, location_start_id, start_time) VALUES ((SELECT MAX(rent_id)+1 FROM rent) , %d , %d , %d , '%s')" % (customer_id,bycicle_id, location_start_id, start_time)
        sql_bike = "UPDATE bycicle SET is_rent = 1  WHERE bycicle_id = %d" % (bycicle_id)
       
        try :
            cursor.execute( sql)   
            rent_id = cursor.lastrowid
            cursor.execute( sql_bike)
            db.commit()
            return [True, str(rent_id)]
        except Exception as e:
            return [False, "Error : "+ str(e) ]
        finally:
             db.close()
    
     #Get Rent by ID
     # Return : rent_id, customer_id, customer_name, bycicle_id, location_start_id, location_start_name, city_start,  
     #          location_end_id, location_end_name, city_end, start_time, end_time, charge, paid, paid_date
    def GetRentById(self, rent_id):
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
        sql = "SELECT r.rent_id, r.customer_id,u.name customer_name, r.bycicle_id, r.location_start_id, ls.location_name location_start_name,cs.city_name city_start,   r.location_end_id, le.location_name location_end_name, ce.city_name city_end, r.start_time, r.end_time, r.charge, r.paid, r.paid_date \
            FROM rent r \
            LEFT JOIN locations ls ON  r.location_start_id = ls.location_id   \
            LEFT JOIN locations le ON  r.location_start_id = le.location_id   \
            LEFT JOIN users u ON u.user_id = r.customer_id \
            LEFT JOIN city cs ON cs.city_id = ls.city_id \
            LEFT JOIN city ce ON ce.city_id = ls.city_id \
            WHERE rent_id = %d" % (rent_id)       
       
        try :
           cursor.execute( sql)  
           return cursor.fetchall()
        except Exception as e:
            return [False, "Error : "+ str(e) ]
        finally:
             db.close()
             
    #Get Rent by Customer ID
    # Return : rent_id, customer_id,customer_name, bycicle_id, location_start_name, city_start,   start_time
    def GetRentByCust(self, cust_id):
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
        sql = "SELECT r.rent_id, r.customer_id,u.name customer_name, r.bycicle_id, ls.location_name location_start_name,cs.city_name city_start,   r.start_time \
            FROM rent r \
            LEFT JOIN locations ls ON  r.location_start_id = ls.location_id   \
            LEFT JOIN users u ON u.user_id = r.customer_id \
            LEFT JOIN city cs ON cs.city_id = ls.city_id \
            WHERE paid IS NULL AND customer_id = %d" % (cust_id)       
       
        try :
           cursor.execute( sql)  
           return cursor.fetchall()
        except Exception as e:
            return [False, "Error : "+ str(e) ]
        finally:
             db.close()
    
    # Return a Bike
    def ReturnBike(self,rent_id, location_end_id, end_time):
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
        sql = "UPDATE rent SET location_end_id = %d, end_time = '%s' WHERE rent_id = %d" % (location_end_id, end_time, rent_id)
        sql_bike = "UPDATE bycicle SET is_rent = 0 WHERE bycicle_id = (SELECT bycicle_id FROM rent WHERE rent_id = %d )" % (rent_id)
        try :
            cursor.execute( sql)
            cursor.execute( sql_bike)
            db.commit()
            return [True, "Success!"]
        except Exception as e:
            return [False, "Error : "+ str(e)]
        finally:
             db.close()
    
     # Get Charge  :     Charge = Charge_rate * minutes spent
    def GetCharge(self, rent_id):
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
        try :
            sql_i = "SELECT bycicle_id, start_time, end_time FROM rent WHERE rent_id = %d" % (rent_id)
            cursor.execute( sql_i) 
            info =  cursor.fetchone()
            bycicle_id = info[0]
            start_time = info[1] 
            end_time = info[2] 
            
            sql = "SELECT  charge_rate FROM bycicle WHERE bycicle_id = %d" % (bycicle_id)
            cursor.execute( sql)  
            rate = cursor.fetchone()[0]
            minute_spent =  (datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')).total_seconds()/ 60
            return rate * minute_spent 
        except Exception as e:
            return [False, "GetCharge Error : "+ str(e)]
        finally:
             db.close()
             
    # Pay a charge
    # Return :  [True, "Success!"], [False, "Error : ..."]
    def PayCharge(self, rent_id, paid, paid_date):
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
        try :
            charge = self.GetCharge(rent_id)
            sql = "UPDATE rent SET charge = %f, paid = %f , paid_date= '%s' WHERE rent_id = %d" % (charge, paid, paid_date, rent_id)
            cursor.execute( sql) 
            db.commit()
            return [True, "Success!"]
        except Exception as e:
            return [False, "Error : "+ str(e)]
        finally:
             db.close()
             
    #Attempts to repair a bike from its ID, returns a boolean indicating if it was successful
    def RepairBike(self, bycicle_id):   
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
        
        try:                
            if not self.IsBycicleIDValid(bycicle_id) or not self.IsBikeDefective(bycicle_id):
                 return False
                    
            cursor.execute("""UPDATE bycicle
                           SET is_repaired = '1', is_defective = '0'
                            WHERE bycicle_id = ?""",[bycicle_id])
            db.commit() 
                
            return True
            
        except:
            return False
        finally:   
            #Always close the db
            db.close()
    
    #Attempts to repair bikes from a list of bikes, returns a list of any bikes that did not update
    def RepairBikes(self, bycicle_ids):
        failedToUpdate = []
        for bycicle_id in bycicle_ids:     
            if not self.RepairBike(bycicle_id):
                failedToUpdate.append(bycicle_id)
        
        return failedToUpdate
    
    #Used to report that the bike is faulty
    def ReportBike(self, bycicle_id):
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
            
        try:           
            if not self.IsBycicleIDValid(bycicle_id) or self.IsBikeDefective(bycicle_id):
                return False
                       
            cursor.execute("""UPDATE bycicle
                           SET is_defective = '1',is_repaired = '0'
                           WHERE bycicle_id = ?""",[bycicle_id])
            db.commit()
            return True
        except:
            return False
        finally:
            db.close()   
             
    def MoveBike(self, bycicle_id, new_location_id, new_position_long, new_position_lat):          
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
            
        if not self.IsLocationIDValid(new_location_id) or not self.IsBycicleIDValid(bycicle_id) or self.IsBikeAlreadyAtThisLocation(bycicle_id,new_location_id):
            return False
                
        try:
            cursor.execute("""UPDATE bycicle
                           SET location_id = ?, current_position_long = ?, current_position_lat = ?
                           WHERE bycicle_id =?""",([new_location_id,new_position_long,new_position_lat, bycicle_id])) 
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
             db.close()  
        
    def IsBycicleIDValid(self,bycicle_id):
       with sqlite3.connect(self.dbaddress) as db: 
           cursor=db.cursor() 
       try:
           sql = """SELECT bycicle_id FROM bycicle WHERE bycicle_id = ?"""
           cursor.execute(sql,[bycicle_id])
           if cursor.fetchone() == None:
               return False
           
           return True
       except:
           return False
       finally:
           db.close()
           
    def IsBikeAlreadyAtThisLocation(self,bycicle_id, new_location_id):
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
        try:
             sql = "SELECT location_id FROM bycicle WHERE bycicle_id = ?"
             cursor.execute(sql,[bycicle_id])
             
             current_location = cursor.fetchone()[0]
             if current_location == None:
                 return False

             return current_location == new_location_id
        except:
             return False
        finally:
             db.close()     
           
    def IsLocationIDValid(self,location_id):
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
        try:
            sql = "SELECT location_name FROM locations WHERE location_id = ?"
            cursor.execute(sql,[location_id])
            if cursor.fetchone() == None:
                return False
        
            return True
        except:
            return False
        finally:
            db.close()
            
    def IsBikeDefective(self, bycicle_id):
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
        try:
            cursor.execute("""SELECT is_defective, is_repaired 
                           FROM bycicle 
                           WHERE bycicle_id = ?""",[bycicle_id]) 
                           
            is_defective,is_repaired = cursor.fetchone()
            
            if(is_defective == 1):
                return True
        
            return False
        except:
            return False
        finally:
            db.close()
           
    # Track Bikes based on location id or city id
    #Return : b.bycicle_id, l.location_id, l.location_name , l.city_id, c.city_name , is_defective , is_rent,is_repaired    
    def TrackBikes (self, location_id="all", city_id="all"):
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
        try:
            sql = "SELECT b.bycicle_id, l.location_id, l.location_name , l.city_id, c.city_name , is_defective , is_rent,is_repaired  FROM bycicle b INNER JOIN locations l ON l.location_id = b.location_id INNER JOIN city c ON c.city_id = l.city_id "
            cond = []       
            if location_id != "all":
                cond.append( " b.location_id = %d " % (location_id))
            if city_id != "all":
                cond.append( " c.city_id = %d " % (city_id))
            cursor.execute( sql+ (" WHERE "+ " AND ".join(cond) if cond != [] else ""))  
            return cursor.fetchall()  
        except Exception as e:
            return [False, "Error : "+ str(e)]
        finally:
             db.close()
    
    # Validate user login
    # Return : user_id, role_id, role_name, name, phone_number, email
    def ValidateUser(self, username, pwd):
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
        try:
            sql = "SELECT u.user_id, u.role_id, r.role_name, u.name, u.phone_number, u.username FROM users u INNER JOIN roles r ON r.role_id = u.role_id WHERE u.username = '%s' AND u.pwd = '%s'" % (username, pwd)            
            #print (sql)
            cursor.execute( sql)  
            arr = cursor.fetchone()  
            if arr == [] :
                return [False, "User not found"]
            else :
                return arr
        except Exception as e:
            return [False, "Error : "+ str(e)]
        finally:
             db.close()
             
    #Insert Bike Rent 
    def AddCustomer(self, username, name, password, phone):
        with sqlite3.connect(self.dbaddress) as db: 
            cursor=db.cursor() 
        sql_user = "SELECT * FROM users WHERE username = '%s'" % (username)        
        sql = "INSERT INTO users (user_id, role_id,username,pwd, name, phone_number) VALUES ((SELECT MAX(user_id)+1 FROM users) ,1, '%s' , '%s' , '%s' , '%s')" % (username,password, name, phone)
               
        try :
            cursor.execute( sql_user) 
            arr = cursor.fetchone()  
            if arr == [] or arr == None:
                cursor.execute( sql)
                db.commit()
                return [True, "You are successfully registered!"]
            else :
                return [False, "Username already exists!"]
            
        except Exception as e:
            return [False, "Error : "+ str(e) ]
        finally:
             db.close()
    
    def GetBikeUsageInfo(self):
        with sqlite3.connect("bike.db") as db: 
            cursor=db.cursor() 
        try:
            sql = "SELECT is_defective, is_rent FROM bycicle"
            cursor.execute(sql)  
            slices = []
            slices.append(PieSlice("Defective","r"))
            slices.append(PieSlice("Rented","darkorange"))
            slices.append(PieSlice("Available","lime"))

            for bycicle in cursor.fetchall():
                is_defective, is_rent = bycicle;

                if is_defective == 1:
                    slices[0].AddValue(1)
                elif is_rent == 1:
                    slices[1].AddValue(1)
                else:
                     slices[2].AddValue(1)
            
            labels = []
            colors = [] 
            values = [] 
            explode = []
            
            for i in slices:
                value = i.GetValue()
                if not value == 0:
                    labels.append(i.GetLabel())
                    colors.append(i.GetColor())
                    values.append(value)
                    explode.append(i.GetExplode())
            return labels,colors,values,explode
        except:
            return None
        finally:
            db.close()
            
    def GetBikeLocationInfo(self):
        with sqlite3.connect("bike.db") as db: 
            cursor=db.cursor() 
        try:
            sql = "SELECT location_name, location_id FROM locations ORDER BY location_name ASC"
            cursor.execute(sql)  
            location_names = []
            counts =[]
            for location in cursor.fetchall():
                location_name, location_id = location;
                location_names.append(location_name)
                sql = "SELECT COUNT(*) FROM bycicle WHERE location_id =" + str(location_id)
                cursor.execute(sql)  
                for count in cursor.fetchone():
                    counts.append(count)
                    
            return location_names, counts
        except:
            return None
        finally:
            db.close()
            
class PieSlice():
    def __init__(self, label, color, value = 0, explode = 0.1):
        self.label = label
        self.color = color
        self.value = value   
        self.explode = explode  

    def AddValue(self,value):
        self.value += value
    
    def GetValue(self):
        return self.value
    
    def GetLabel(self):
        return self.label
    
    def GetExplode(self):
        return self.explode
    
    def GetColor(self):
        return self.color
    
def main(): 
    a = Backend()
    print(a.AddCustomer("nurul", "Nurul", "nurul", "0988"))
    

    
if __name__ == "__main__":
    main()
