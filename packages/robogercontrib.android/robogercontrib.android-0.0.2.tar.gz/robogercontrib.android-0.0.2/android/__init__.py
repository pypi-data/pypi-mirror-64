import filetype

from types import SimpleNamespace
from pyfcm import FCMNotification

from roboger.core import logger, bucket_put

_cfg = SimpleNamespace(api_key=None, registration_id=None, device_id=None)


def load(plugin_config, **kwargs):
    if not all(list(plugin_config.values())):
        er = ', '.join([e for e in plugin_config if plugin_config[e] is None])
        logger.error(f'{er} is empty')
    else:
        try:
            _cfg.push_service = FCMNotification(
                api_key=plugin_config.pop('api_key'))
        except Exception as e:
            logger.error(f'{__name__} Failed create FCMNotification')
        _cfg.registration_id, _cfg.device_id = list(plugin_config.values())


def send(config, event_id, addr_id, msg, subject, formatted_subject, sender,
         location, media, media_fname, level, **kwargs):
    if _cfg.registration_id:
        if not sender:
            sender = 'roboger'
        data = {'location': location, 'sender': sender, 'level': level,
                'subject': subject, 'id': event_id, 'msg': msg}
        if media:
            ft = filetype.guess(media)
            try:
                object_id = bucket_put(content=media, creator='test',
                                       addr_id=addr_id, public=True,
                                       fname=media_fname if media_fname
                                       else None)
            except Exception as e:
                logger.warning(
                    'saving image for event %s. Exception %s' % event_id, e)
            else:
                data['media'] = {'type': (ft.extension if ft else 'Unknown'),
                                 'data': object_id}
            logger.info('sending event %s' % (event_id))
        try:
            logger.info(
                'Android endpoint sending event to %s' % _cfg.registration_id)
            _cfg.push_services.single_device_data_message(
                registration_id=_cfg.registration_id, data_message=data)
        except:
            logger.warning('failed to send event %s via endpoint %u'
                           % event_id)
            return False
    else:
        logger.error(f'{__name__} {event_id} ignored, not active')
