import time
import uuid

from .report import Report
from .services import *


class InvalidSpecification(Exception):
    pass


# used to get named specification dictionary from tuple, using auto-exception if needed
def _sep_spec(_spec: tuple, names: tuple[str] | tuple) -> dict:
    if len(_spec) == len(names):
        return dict(zip(names, _spec))
    else:
        raise InvalidSpecification()


def inspect(spec) -> Report:
    spec = _sep_spec(spec, ())  # no specification

    rep = Report('INSPECT')
    rep.record('INSPECT started!', __name__)
    jars_dict = mm_storage.list_jars(rep)  # get jars dict

    if jars_dict:
        jars = '\n'.join(list(f'{key.upper()}: {jars_dict[key]}' for key in jars_dict))
        rep.result = jars
    else:  # if jars_dict empty
        rep.result = '.jar files not found!'

    rep.record('INSPECT ended!', __name__)

    return rep
    # raise NotImplementedError('INSPECT is not implemented!')


def peer(spec) -> Report:
    spec = _sep_spec(spec, ('listed_id',))

    listed_id = spec['listed_id'].lower()  # listed id stored and used in lowercase

    rep = Report('PEER')
    rep.record('PEER started!', __name__)
    rep.record(f'PEER spec: {" ".join(spec)}', __name__)

    jar = mm_storage.get_jar(listed_id, rep)  # request jar

    if jar:
        mod = extractor.extract_info(jar, rep)  # extract mod info rom jar

        if mod:
            rep.result = f"""\
Minecraft {mod.name} {mod.version}:
-- {mod.description} --
ID: {mod.modid}
Minecraft compatible version: {mod.dependencies[0].version} {mod.loader}"""

        else:
            rep.result = 'This .jar is not valid minecraft mod!'

    else:
        rep.result = f'Bad listed id or wrong file format! ({listed_id})'

    rep.record('PEER ended!', __name__)

    return rep

    # raise NotImplementedError('PEER is not implemented!')


def expel(spec):
    spec = _sep_spec(spec, ('listed_id',))

    listed_id = spec['listed_id'].lower()  # listed id stored and used in lowercase

    rep = Report('EXPEL')
    rep.record('EXPEL started!', __name__)
    rep.record(f'EXPEL spec: {" ".join(spec)}', __name__)

    status = mm_storage.delete_jar(listed_id, rep)  # delete .jar
    if status:
        rep.result = f'.jar deleted successfully! (listed id: {listed_id.upper()})'
    else:
        rep.result = 'Unable to delete .jar!'

    rep.record('EXPEL ended!', __name__)

    return rep

    # raise NotImplementedError('EXPEL is not implemented!')


def adopt(spec):
    spec = _sep_spec(spec, ('listed_id',))

    listed_id = spec['listed_id'].lower()  # listed id stored and used in lowercase

    rep = Report('ADOPT')
    rep.record('ADOPT started!', __name__)
    rep.record(f'ADOPT spec: {" ".join(spec)}', __name__)

    jar = mm_storage.get_jar(listed_id, rep)  # request jar

    if jar:
        mod = extractor.extract_info(jar, rep)

        saved_id = jar_keeper.save(
            jar,
            (f'{mod.name} {mod.version}' if mod
             else input('This .jar file isn\'t Minecraft valid mod! Provide name: ')),
            rep)
        rep.result = f'Requested .jar saved! ID: {saved_id.upper()}'
    else:  # if .jar not found
        rep.result = f'Bad listed id! ({listed_id.upper()})'

    rep.record('ADOPT ended!', __name__)

    return rep

    # raise NotImplementedError('ADOPT is not implemented!')


def adopts(spec):
    spec = _sep_spec(spec, ())  # no specification

    rep = Report('ADOPTS')
    rep.record('ADOPTS started!', __name__)
    rep.record(f'ADOPTS spec: {" ".join(spec)}', __name__)

    # convert id
    ids = jar_keeper.get_ids(rep)
    ids_s = jar_keeper.get_ids_simplified(list(ids.keys()), rep)

    if ids:
        rep.result = '\n'.join(f'{ids_s[i].upper()}: {ids[i]}' for i in ids)  # generate string from saved mods dict
    else:  # if ids empty
        rep.result = 'Did not get any saved ids!'

    rep.record('ADOPTS ended!', __name__)

    return rep

    # raise NotImplementedError('ADOPTS is not implemented!')


def release(spec):
    spec = _sep_spec(spec, ('saved_id',))

    saved_id = spec['saved_id'].lower()  # saved id stored and used in lowercase

    rep = Report('RELEASE')
    rep.record('RELEASE started!', __name__)
    rep.record(f'RELEASE spec: {" ".join(spec)}', __name__)

    # convert id
    ids = jar_keeper.get_ids(rep)
    ids_s = jar_keeper.get_ids_simplified(list(ids.keys()), rep)
    saved_id = jar_keeper.get_true_id(ids_s, saved_id, rep)

    # main part
    jar, status = jar_keeper.load(saved_id, rep)
    if status and saved_id in ids:  # saved id check
        name = time.strftime('%Y%m%d%H%M%S', time.gmtime()) + extractor.extract_info(jar, rep).modid  # generate uniq id
        status = mm_storage.insert_jar(jar, name, rep)  # insert
        if status:
            rep.result = f'Requested .jar released! (filename: {name}.jar)'
        else:  # logically should not happen, but you never know
            rep.result = f'Requested .jar could not be released!'
    else:
        rep.result = f'Bad saved id! ({saved_id.upper()})'

    rep.record('RELEASE ended!', __name__)

    return rep

    # raise NotImplementedError('RELEASE is not implemented!')


def punish(spec):
    spec = _sep_spec(spec, ('saved_id',))

    saved_id = spec['saved_id'].lower()  # saved id stored and used in lowercase

    rep = Report('PUNISH')
    rep.record('PUNISH started!', __name__)
    rep.record(f'PUNISH spec: {" ".join(spec)}', __name__)

    # convert id
    ids = jar_keeper.get_ids(rep)
    ids = jar_keeper.get_ids_simplified(list(ids.keys()), rep)
    saved_id = jar_keeper.get_true_id(ids, saved_id, rep)
    if not saved_id:
        rep.result = f'Bad saved id! ({saved_id.upper()})'

    status = jar_keeper.delete(saved_id, rep)  # delete

    if status:
        rep.result = 'Requested .jar unsaved!'
    else:
        rep.result = f'Bad saved id! ({saved_id.upper()})'

    return rep

    # raise NotImplementedError('PUNISH is not implemented!')


def bundle(spec):
    spec = _sep_spec(spec, ('name',))

    rep = Report('BUNDLE')
    rep.record('BUNDLE started!', __name__)
    rep.record(f'BUNDLE spec: {" ".join(spec)}', __name__)

    # save initial bundle data
    bundle_id = uuid.uuid4().hex
    bundle_obj = []  # BINDed mods ids will be here
    pickler.remember(bundle_obj, bundle_id, rep, '\\bundles')

    # save bundle id
    bundle_ids_saved = pickler.recall('bundle_ids', rep)
    if not bundle_ids_saved:  # if found nothing saved
        bundle_ids_saved = {}
    bundle_ids_saved[bundle_id] = spec['name']
    pickler.remember(bundle_ids_saved, 'bundle_ids', rep)

    rep.result = f'Bundle created successfully! (id: {str(uuid.UUID(bundle_id)).upper()})'

    rep.record('BUNDLE ended!', __name__)

    return rep

    # raise NotImplementedError('BUNDLE is not implemented!')


def bundles(spec):
    spec = _sep_spec(spec, ())

    rep = Report('BUNDLES')
    rep.record('BUNDLES started!', __name__)

    # load saved bundles ids
    bundle_ids_saved = pickler.recall('bundle_ids', rep)
    if not bundle_ids_saved:  # if found nothing saved
        bundle_ids_saved = {}
        rep.result = 'Unable to list bundles!'
    else:
        rep.result = '\n'.join(f'{str(uuid.UUID(key)).upper()}: {bundle_ids_saved[key]}' for key in bundle_ids_saved)

    rep.record('BUNDLES ended!', __name__)

    return rep

    # raise NotImplementedError('BUNDLES is not implemented!')


def burst(spec):
    spec = _sep_spec(spec, ('id',))

    rep = Report('BURST')
    rep.record('BURST started!', __name__)
    rep.record(f'BURST spec: {" ".join(spec)}', __name__)

    try:
        spec['id'] = uuid.UUID(spec['id']).hex
    except ValueError:
        rep.result = 'Wrong ID type!'
        return rep

    # load saved bundles ids
    bundle_ids_saved = pickler.recall('bundle_ids', rep)
    if not bundle_ids_saved:  # if found nothing saved
        bundle_ids_saved = {}

    name = bundle_ids_saved.pop(spec['id'], None)
    if name:
        pickler.remember(bundle_ids_saved, 'bundle_ids', rep)
        rep.result = f'Bundle {name} bursted!'
    else:
        rep.result = f'Unable to burst bundle! (not found)'

    rep.record('BURST ended!', __name__)

    return rep

    # raise NotImplementedError('BURST is not implemented!')


def bind(spec):
    spec = _sep_spec(spec, ('id', 'saved_id',))

    saved_id = spec['saved_id'].lower()  # saved id stored and used in lowercase

    rep = Report('BIND')
    rep.record('BIND started!', __name__)
    rep.record(f'BIND spec: {" ".join(spec)}', __name__)

    # convert bundle id
    try:
        spec['id'] = uuid.UUID(spec['id']).hex
    except ValueError:
        rep.result = 'Wrong ID type!'
        rep.record('BIND ended!', __name__)
        return rep

    # convert saved id
    ids = jar_keeper.get_ids(rep)
    ids = jar_keeper.get_ids_simplified(list(ids.keys()), rep)
    saved_id = jar_keeper.get_true_id(ids, saved_id, rep)
    if not saved_id:
        rep.result = f'Bad saved id! ({saved_id.upper()})'
        rep.record('BIND ended!', __name__)
        return rep

    # load saved bundle data
    bundle_obj = pickler.recall(spec['id'], rep, '\\bundles')
    if bundle_obj is None:
        rep.result = f'Bad bundle id! ({spec["id"]})'
        rep.record('BIND ended!', __name__)
        return rep

    # add id
    bundle_obj.append(saved_id)
    pickler.remember(bundle_obj, spec['id'], rep, '\\bundles')

    # load saved bundles ids
    bundle_ids_saved = pickler.recall('bundle_ids', rep)
    if not bundle_ids_saved:  # if found nothing saved
        bundle_ids_saved = {}

    rep.result = f'Saved id {saved_id.upper()} binded to bundle {bundle_ids_saved[spec["id"]]}!'

    rep.record('BIND ended!', __name__)
    return rep

    # raise NotImplementedError('BIND is not implemented!')


def detach(spec):
    raise NotImplementedError('DETACH is not implemented!')


def apply(spec):
    raise NotImplementedError('APPLY is not implemented!')
