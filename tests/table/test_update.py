import datetime
from unittest import TestCase

from piccolo.columns.column_types import Timestamp, Varchar
from piccolo.table import Table
from tests.base import DBTestCase, postgres_only
from tests.example_apps.music.tables import Band, Poster


class TestUpdate(DBTestCase):
    def check_response(self):
        response = (
            Band.select(Band.name)
            .where(Band.name == "Pythonistas3")
            .run_sync()
        )

        self.assertEqual(response, [{"name": "Pythonistas3"}])

    def test_update(self):
        """
        Make sure updating work, when passing the new values directly to the
        `update` method.
        """
        self.insert_rows()

        Band.update({Band.name: "Pythonistas3"}).where(
            Band.name == "Pythonistas"
        ).run_sync()

        self.check_response()

    def test_update_with_string_keys(self):
        """
        Make sure updating work, when passing a dictionary of values, which
        uses column names as keys, instead of Column instances.
        """
        self.insert_rows()

        Band.update({"name": "Pythonistas3"}).where(
            Band.name == "Pythonistas"
        ).run_sync()

        self.check_response()

    def test_update_with_kwargs(self):
        """
        Make sure updating work, when passing the new value via kwargs.
        """
        self.insert_rows()

        Band.update(name="Pythonistas3").where(
            Band.name == "Pythonistas"
        ).run_sync()

        self.check_response()

    def test_update_values(self):
        """
        Make sure updating work, when passing the new values via the `values`
        method.
        """
        self.insert_rows()

        Band.update().values({Band.name: "Pythonistas3"}).where(
            Band.name == "Pythonistas"
        ).run_sync()

        self.check_response()

    def test_update_values_with_string_keys(self):
        """
        Make sure updating work, when passing the new values via the `values`
        method, using a column name as a dictionary key.
        """
        self.insert_rows()

        Band.update().values({"name": "Pythonistas3"}).where(
            Band.name == "Pythonistas"
        ).run_sync()

        self.check_response()

    def test_update_values_with_kwargs(self):
        """
        Make sure updating work, when passing the new values via kwargs.
        """
        self.insert_rows()

        Band.update().values(name="Pythonistas3").where(
            Band.name == "Pythonistas"
        ).run_sync()

        self.check_response()


class TestIntUpdateOperators(DBTestCase):
    def test_add(self):
        self.insert_row()

        Band.update(
            {Band.popularity: Band.popularity + 10}, force=True
        ).run_sync()

        response = Band.select(Band.popularity).first().run_sync()

        self.assertEqual(response["popularity"], 1010)

    def test_add_column(self):
        self.insert_row()

        Band.update(
            {Band.popularity: Band.popularity + Band.popularity}, force=True
        ).run_sync()

        response = Band.select(Band.popularity).first().run_sync()

        self.assertEqual(response["popularity"], 2000)

    def test_radd(self):
        self.insert_row()

        Band.update(
            {Band.popularity: 10 + Band.popularity}, force=True
        ).run_sync()

        response = Band.select(Band.popularity).first().run_sync()

        self.assertEqual(response["popularity"], 1010)

    def test_sub(self):
        self.insert_row()

        Band.update(
            {Band.popularity: Band.popularity - 10}, force=True
        ).run_sync()

        response = Band.select(Band.popularity).first().run_sync()

        self.assertEqual(response["popularity"], 990)

    def test_rsub(self):
        self.insert_row()

        Band.update(
            {Band.popularity: 1100 - Band.popularity}, force=True
        ).run_sync()

        response = Band.select(Band.popularity).first().run_sync()

        self.assertEqual(response["popularity"], 100)

    def test_mul(self):
        self.insert_row()

        Band.update(
            {Band.popularity: Band.popularity * 2}, force=True
        ).run_sync()

        response = Band.select(Band.popularity).first().run_sync()

        self.assertEqual(response["popularity"], 2000)

    def test_rmul(self):
        self.insert_row()

        Band.update(
            {Band.popularity: 2 * Band.popularity}, force=True
        ).run_sync()

        response = Band.select(Band.popularity).first().run_sync()

        self.assertEqual(response["popularity"], 2000)

    def test_div(self):
        self.insert_row()

        Band.update(
            {Band.popularity: Band.popularity / 10}, force=True
        ).run_sync()

        response = Band.select(Band.popularity).first().run_sync()

        self.assertEqual(response["popularity"], 100)

    def test_rdiv(self):
        self.insert_row()

        Band.update(
            {Band.popularity: 1000 / Band.popularity}, force=True
        ).run_sync()

        response = Band.select(Band.popularity).first().run_sync()

        self.assertEqual(response["popularity"], 1)


class TestVarcharUpdateOperators(DBTestCase):
    def test_add(self):
        self.insert_row()

        Band.update({Band.name: Band.name + "!!!"}, force=True).run_sync()

        response = Band.select(Band.name).first().run_sync()

        self.assertEqual(response["name"], "Pythonistas!!!")

    def test_add_column(self):
        self.insert_row()

        Band.update({Band.name: Band.name + Band.name}, force=True).run_sync()

        response = Band.select(Band.name).first().run_sync()

        self.assertEqual(response["name"], "PythonistasPythonistas")

    def test_radd(self):
        self.insert_row()

        Band.update({Band.name: "!!!" + Band.name}, force=True).run_sync()

        response = Band.select(Band.name).first().run_sync()

        self.assertEqual(response["name"], "!!!Pythonistas")


class TestTextUpdateOperators(DBTestCase):
    def setUp(self):
        super().setUp()
        Poster(content="Join us for this amazing show").save().run_sync()

    def test_add(self):
        Poster.update(
            {Poster.content: Poster.content + "!!!"}, force=True
        ).run_sync()

        response = Poster.select(Poster.content).first().run_sync()

        self.assertEqual(
            response["content"], "Join us for this amazing show!!!"
        )

    def test_add_column(self):
        self.insert_row()

        Poster.update(
            {Poster.content: Poster.content + Poster.content}, force=True
        ).run_sync()

        response = Poster.select(Poster.content).first().run_sync()

        self.assertEqual(
            response["content"],
            "Join us for this amazing show" * 2,
        )

    def test_radd(self):
        self.insert_row()

        Poster.update(
            {Poster.content: "!!!" + Poster.content}, force=True
        ).run_sync()

        response = Poster.select(Poster.content).first().run_sync()

        self.assertEqual(
            response["content"], "!!!Join us for this amazing show"
        )


class Concert(Table):
    name = Varchar()
    starts = Timestamp()


# TODO - add SQLite support
@postgres_only
class TestTimestampUpdateOperators(TestCase):

    delta = datetime.timedelta(
        days=1, hours=1, minutes=1, seconds=30, microseconds=500
    )

    def setUp(self):
        Concert.create_table().run_sync()
        Concert.insert(
            Concert(
                name="Royal Albert Hall",
                starts=datetime.datetime(
                    year=2022, month=1, day=1, hour=21, minute=0
                ),
            )
        ).run_sync()

    def tearDown(self):
        Concert.alter().drop_table().run_sync()

    def test_add(self):
        query = Concert.update(
            {Concert.starts: Concert.starts + self.delta},
            force=True,
        )
        query.run_sync()

        new_start_value = (
            Concert.select(Concert.starts).first().run_sync()["starts"]
        )
        self.assertEqual(
            new_start_value,
            datetime.datetime(
                year=2022,
                month=1,
                day=2,
                hour=22,
                minute=1,
                second=30,
                microsecond=500,
            ),
        )

    def test_radd(self):
        query = Concert.update(
            {Concert.starts: self.delta + Concert.starts},
            force=True,
        )
        query.run_sync()

        new_start_value = (
            Concert.select(Concert.starts).first().run_sync()["starts"]
        )
        self.assertEqual(
            new_start_value,
            datetime.datetime(
                year=2022,
                month=1,
                day=2,
                hour=22,
                minute=1,
                second=30,
                microsecond=500,
            ),
        )

    def test_substract(self):
        query = Concert.update(
            {Concert.starts: Concert.starts - self.delta},
            force=True,
        )
        query.run_sync()

        new_start_value = (
            Concert.select(Concert.starts).first().run_sync()["starts"]
        )
        self.assertEqual(
            new_start_value,
            datetime.datetime(
                year=2021,
                month=12,
                day=31,
                hour=19,
                minute=58,
                second=29,
                microsecond=999500,
            ),
        )
