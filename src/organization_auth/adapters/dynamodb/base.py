from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, DiscriminatorAttribute, UTCDateTimeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection


class ClassesIndex(GlobalSecondaryIndex):
    """Index for incrising performance for queries

    Optimized queries are:
    - Get all teams
    - Get a user by id
    - Get a group by id
    """
    class Meta:
        index_name = 'cls-index'
        read_capacity_units = 2
        write_capacity_units = 1
        projection = AllProjection()

    sk_id = UnicodeAttribute(hash_key=True)


class DDBOrganizationModel(Model):
    """Base Table

    Primary key and Sort key schemas per entity:

    Team 			pk=team_id 		sk=Team
    User			pk=team_id 		sk=User-<user_id>
    Group 	        pk=team_id 		sk=Group-<group_id>
    UserInGroup		pk=team_id 		sk=<group_id>#<user_id>
    """
    class Meta:
        table_name = "DDBOrganizationModel"
        host = "http://localhost:4566"
        region = "us-east-1"

    pk_id = UnicodeAttribute(hash_key=True)
    sk_id = UnicodeAttribute(range_key=True)

    created_at = UTCDateTimeAttribute()
    updated_at = UTCDateTimeAttribute()

    cls = DiscriminatorAttribute()

    classes_index = ClassesIndex()
