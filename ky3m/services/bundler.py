import uuid

from ky3m.report import Report

from . import pickler as pcl


# load saved bundles ids
def get_bundle_ids(_rep: Report) -> dict:
    bundle_ids_saved = pcl.recall('bundle_ids', _rep)
    if not bundle_ids_saved:  # if found nothing saved
        bundle_ids_saved = {}
        _rep.record(f'bundle ids not found!', __name__)
    else:
        _rep.record(f'got bundle ids!', __name__)
    return bundle_ids_saved


# create bundle
def create_bundle(name: str, _rep: Report) -> uuid.UUID:
    # save initial bundle data
    bundle_id = uuid.uuid4().hex
    bundle_obj = []  # BINDed mods ids will be here
    pcl.remember(bundle_obj, bundle_id, _rep, '\\bundles')

    # save bundle id
    bundle_ids_saved = get_bundle_ids(_rep)
    bundle_ids_saved[bundle_id] = name
    pcl.remember(bundle_ids_saved, 'bundle_ids', _rep)
    _rep.record(f'bundle created! (name: {name}, id: {bundle_id})', __name__)

    return uuid.UUID(bundle_id)
