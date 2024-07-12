from hishel import CacheClient, Controller, FileStorage

controller = Controller(
    cacheable_methods=["GET", "POST"],
    cacheable_status_codes=[200],
    allow_stale=True,
    always_revalidate=True,
)
storage = FileStorage(ttl=900)
client = CacheClient(controller=controller, storage=storage)
