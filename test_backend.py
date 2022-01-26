import unittest
import sqlite3
import Backend

# Customers should be able to:
# o Rent a bike at any location in the city, as long as there is a
# working bike available at that location. (2 marks)
# o Return a bike to any location. When a customer returns a
# bike, their account is charged an amount depending on
# how long the bike rental was. (2 marks)
# o Report a bike as defective. (1 mark)
# o Pay any charges on their account. (1 mark)


class TestCostmers(unittest.TestCase):

    # rent a bike any location
    def test_AddBikeRent(self):
        db_addr = "test_db/AddBikeRent.db"
        b = Backend.Backend(db_addr)

        customer_id, bycicle_id, location_start_id, start_time = 1, 2, 3, '2021-26-01 17:00'
        b.AddBikeRent(customer_id, bycicle_id, location_start_id, start_time)
        datas = (customer_id, bycicle_id, location_start_id, start_time)

        sql_inquire = """
            SElECT customer_id,bycicle_id, location_start_id, start_time 
            from rent
            WHERE customer_id = %d""" % datas[0]

        sql_clean = """
            delete from rent
        """

        with sqlite3.connect(db_addr) as db:
            cursor = db.cursor()

            cursor.execute(sql_inquire)
            record = cursor.fetchall()
            try:
                self.assertEqual(record[0], datas)
            finally:
                cursor.execute(sql_clean)
                db.commit()

    # return a bike to any location
    def test_ReturnBike(self):
        db_addr = "test_db/ReturnBike.db"
        b = Backend.Backend(db_addr)

        rent_id, location_end_id, end_time = 8, 2, '2021-26-01 18:00'
        b.ReturnBike(rent_id, location_end_id, end_time)
        datas = (rent_id, location_end_id, end_time)

        sql_inquire_end_status = """
            SElECT rent_id, location_end_id, end_time
            from rent
            WHERE rent_id = %d""" % rent_id

        sql_clean = """
            UPDATE rent SET location_end_id = NULL, end_time = NULL WHERE rent_id = %d
        """ % rent_id

        with sqlite3.connect(db_addr) as db:
            cursor = db.cursor()

            cursor.execute(sql_inquire_end_status)
            record = cursor.fetchall()
            try:
                self.assertEqual(record[0], datas)
            finally:
                cursor.execute(sql_clean)
                db.commit()

    # their account is charged an amount depending on
    # how long the bike rental was.
    # Pay any charges on their account.
    def test_PayCharge(self):
        db_addr = "test_db/PayCharge.db"
        b = Backend.Backend(db_addr)

        rent_id, paid, paid_date = 4, 3.2, '2021-01-28 17:09'

        b.PayCharge(rent_id, paid, paid_date)
        datas = (rent_id, paid, paid_date)

        sql_inquire_end_status = """
            SElECT rent_id, paid, paid_date
            from rent
            WHERE rent_id = %d""" % rent_id

        sql_clean = """
            UPDATE rent SET paid = NULL, paid_date = NULL, charge = NULL
            WHERE rent_id = %d
            """ % rent_id

        with sqlite3.connect(db_addr) as db:
            cursor = db.cursor()

            cursor.execute(sql_inquire_end_status)
            record = cursor.fetchall()
            try:
                self.assertEqual(record, [datas])
            finally:
                cursor.execute(sql_clean)
                db.commit()

    # Report a bike that doesn't exist as defective.
    def test_ReportBike_donotexist_bike(self):
        db_addr = "test_db/ReportBike.db"
        b = Backend.Backend(db_addr)

        # inqurie a bike do not exist
        self.assertFalse(b.RepairBike(bycicle_id=100))

        # self.assertFalse(b.RepairBike(bycicle_id=3))
        # sql in IsBikeDefective() may have some error

    # Report a bike as defective successfully
    def test_ReportBike(self):
        db_addr = "test_db/ReportBike.db"
        bycicle_id = 2
        b = Backend.Backend(db_addr)
        b.ReportBike(bycicle_id=bycicle_id)

        sql_inquire_end_status = """
            SElECT is_defective
            from bycicle
            WHERE bycicle_id = %d""" % bycicle_id

        sql_clean = """
            UPDATE bycicle SET is_defective = '0'
            WHERE bycicle_id = %d
            """ % bycicle_id

        with sqlite3.connect(db_addr) as db:
            cursor = db.cursor()

            cursor.execute(sql_inquire_end_status)
            record = cursor.fetchall()
            try:
                self.assertEqual(record, [(1,)])
            finally:
                cursor.execute(sql_clean)
                db.commit()


class TestOperators(unittest.TestCase):

    # Track the location of all bikes in the city
    def test_TrackBikes(self):
        db_addr = "test_db/TrackBikes.db"
        b = Backend.Backend(db_addr)
        self.assertEqual(b.TrackBikes(), [
            (1, 1, 'Stat-001', 2, 'Glasgow', 0, 1, 0),
            (2, 10, 'Stat-010', 1, 'Edinburgh', 0, 1, 0),
            (3, 5, 'Stat-005', 2, 'Glasgow', 0, 1, 0)])

    # Repair a defective bike
    def test_RepairBike(self):
        db_addr = "test_db/RepairBike.db"
        b = Backend.Backend(db_addr)

        bycicle_id = 2
        b.RepairBike(bycicle_id=bycicle_id)

        sql_inquire_end_status = """
            SElECT is_repaired, is_defective
            from bycicle
            WHERE bycicle_id = %d""" % bycicle_id

        sql_clean = """
            UPDATE bycicle
            SET is_repaired = '0', is_defective = '1'
            WHERE bycicle_id = %d""" % bycicle_id

        with sqlite3.connect(db_addr) as db:
            cursor = db.cursor()

            cursor.execute(sql_inquire_end_status)
            record = cursor.fetchall()
            try:
                self.assertEqual(record, [(1, 0)])
            finally:
                cursor.execute(sql_clean)
                db.commit()

    # Move bikes to different locations around the city as needed.
    def test_MoveBike(self):
        db_addr = "test_db/MoveBike.db"
        b = Backend.Backend(db_addr)

        bycicle_id, new_location_id, new_position_long, new_position_lat =\
            2, 5, 35, 53
        b.MoveBike(bycicle_id=bycicle_id,
                   new_location_id=new_location_id,
                   new_position_long=new_position_long,
                   new_position_lat=new_position_lat)

        sql_inquire_end_status = """
            SElECT bycicle_id, location_id, current_position_long, current_position_lat
            from bycicle
            WHERE bycicle_id = %d""" % bycicle_id

        sql_clean = """
            UPDATE bycicle
            SET location_id = 10, current_position_long = NULL, current_position_lat = NULL
            WHERE bycicle_id = %d""" % bycicle_id

        with sqlite3.connect(db_addr) as db:
            cursor = db.cursor()

            cursor.execute(sql_inquire_end_status)
            record = cursor.fetchall()
            try:
                self.assertEqual(record,
                                 [(bycicle_id, new_location_id, new_position_long, new_position_lat)])
            finally:
                cursor.execute(sql_clean)
                db.commit()


class TestManagers(unittest.TestCase):

    def test_GetBikeLocationInfo(self):
        db_addr = "test_db/GetBikeLocationInfo.db"
        b = Backend.Backend(db_addr)

        self.assertEqual(b.GetBikeLocationInfo(),
                         (['Stat-001', 'Stat-002', 'Stat-003', 'Stat-004',
                           'Stat-005', 'Stat-006', 'Stat-007', 'Stat-008',
                           'Stat-009', 'Stat-010'],
                          [1, 0, 0, 0, 1, 0, 0, 0, 0, 1]))

    def test_GetBikeUsageInfo(self):
        db_addr = "test_db/GetBikeUsageInfo.db"
        b = Backend.Backend(db_addr)

        self.assertEqual(b.GetBikeUsageInfo(),
                         (['Rented'], ['darkorange'], [3], [0.1]))


if __name__ == '__main__':
    unittest.main()
