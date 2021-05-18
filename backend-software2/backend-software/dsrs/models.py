from django.db import models
from django.contrib.postgres.fields import ArrayField
# Spotify_SpotifyDuo_SGAE_NO_NOK_20200101-20200531.tsv
# Spotify_SpotifyFamilyPlan_SGAE_ES_EUR_20200101-20200331.tsv



class File_dir(models.Model):
    id = models.IntegerField(primary_key=True)
    file_name = models.CharField(max_length = 255)
    path = models.CharField(max_length = 255)
    is_read = models.BooleanField(default=False)
    def get_absolute_url(self):
        return reverse('file_dir')
class Currency(models.Model):
    name = models.CharField(max_length=48)
    symbol = models.CharField(max_length=4)
    code = models.CharField(max_length=3)

    class Meta:
        db_table = "currency"
        verbose_name = "currency"
        verbose_name_plural = "currencies"

class Territory(models.Model):
    name = models.CharField(max_length=48)
    code_2 = models.CharField(max_length=2)
    code_3 = models.CharField(max_length=3)
    local_currency = models.ForeignKey(
        "Currency", related_name="territories", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "territory"
        verbose_name = "territory"
        verbose_name_plural = "territories"
        ordering = ("name",)


class DSR(models.Model):
    class Meta:
        db_table = "dsr"

    STATUS_ALL = (
        ("failed", "FAILED"),
        ("ingested", "INGESTED"),
    )

    path = models.CharField(max_length=256, default = '/path/to/dsr.csv')
    period_start = models.DateField(null=False)
    period_end = models.DateField(null=False)

    status = models.CharField(
        choices=STATUS_ALL, default=STATUS_ALL[1][0], max_length=48
    )

    territory = models.ForeignKey(
        Territory, related_name="dsrs", on_delete=models.CASCADE
    )
    currency = models.ForeignKey(
        Currency, related_name="dsrs", on_delete=models.CASCADE
    )


class Resource(models.Model):
    dsp_id = models.CharField(max_length = 255)
    title = models.CharField(max_length = 255)
    artists = models.CharField(max_length = 255)
    isrc = models.CharField(max_length = 255)
    usages = models.IntegerField(null=True)
    revenue = models.FloatField()
    dsrs = models.CharField(max_length=255)
    dsr_key=models.ForeignKey(DSR, on_delete=models.CASCADE)

