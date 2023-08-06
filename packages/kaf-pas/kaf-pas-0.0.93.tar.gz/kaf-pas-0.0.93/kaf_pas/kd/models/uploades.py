import logging

from bitfield import BitField
from django.db import transaction

from isc_common.bit import TurnBitOn
from isc_common.common import blinkString
from isc_common.common.mat_views import refresh_mat_view
from isc_common.fields.related import ForeignKeyCascade
from isc_common.models.audit import AuditModel, AuditManager, AuditQuerySet
from isc_common.number import DelProps
from isc_common.progress import managed_progress, ProgressDroped
from kaf_pas.kd.models.pathes import Pathes
from kaf_pas.production.models import progress_deleted

logger = logging.getLogger(__name__)


class UploadesQuerySet(AuditQuerySet):
    def create(self, **kwargs):
        return super().create(**kwargs)

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)

class UploadesManager(AuditManager):

    @staticmethod
    def props():
        return BitField(flags=(
            ('confirmed', 'Подтверждено'),
        ), default=0, db_index=True)

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'lastmodified': record.lastmodified,
            'path_id': record.path.id,
            'absolute_path': record.path.absolute_path,
            'editing': record.editing,
            'deliting': record.deliting,
            'props': record.props,
            'confirmed': record.props.confirmed,
        }
        return DelProps(res)

    def get_queryset(self):
        return UploadesQuerySet(self.model, using=self._db)

    def deleteFromRequest(self, request):

        from isc_common.auth.models.user import User
        from isc_common.models.deleted_progresses import Deleted_progresses
        from kaf_pas.ckk.models.item import Item
        from kaf_pas.ckk.models.item import ItemManager
        from kaf_pas.ckk.models.item_image_refs import Item_image_refs
        from kaf_pas.kd.models.document_attr_cross import Document_attr_cross
        from kaf_pas.kd.models.documents import Documents
        from kaf_pas.kd.models.documents_history import Documents_history
        from kaf_pas.kd.models.documents_thumb import Documents_thumb
        from kaf_pas.kd.models.documents_thumb10 import Documents_thumb10
        from kaf_pas.kd.models.lotsman_document_attr_cross import Lotsman_document_attr_cross
        from kaf_pas.kd.models.lotsman_documents_hierarcy import Lotsman_documents_hierarcy
        from kaf_pas.kd.models.lotsman_documents_hierarcy_files import Lotsman_documents_hierarcy_files
        from kaf_pas.kd.models.lotsman_documents_hierarcy_refs import Lotsman_documents_hierarcy_refs
        from kaf_pas.kd.models.uploades_documents import Uploades_documents
        from kaf_pas.kd.models.uploades_log import Uploades_log
        from kaf_pas.production.models.operations_item import Operations_item

        ids = request.GET.getlist('ids')
        user = User.objects.get(username=request.GET.get('ws_channel').split('_')[1])

        res = 0
        for i in range(0, len(ids), 2):
            id = ids[i]
            visibleMode = ids[i + 1]

            if visibleMode != "none":
                res += super().filter(id=id).soft_delete(visibleMode=visibleMode)
            else:
                lotsman_cnt = 0

                for upload_document in Uploades_documents.objects.filter(upload_id=id):
                    lotsman_cnt += Lotsman_documents_hierarcy.objects.filter(document=upload_document.document).count()

                with managed_progress(
                        qty=Uploades_documents.objects.filter(upload_id=id).count() + lotsman_cnt,
                        id=f'Remove_upload_{id}',
                        user=user,
                        message=f'Удаление закачки: {super().get(id=id).path.drived_absolute_path}',
                        title='Выполнено',
                        props=TurnBitOn(0, 0)
                ) as progress:
                    try:
                        with transaction.atomic():
                            lotsman_cnt = 0
                            doc_cnt = 0

                            deleted = Uploades_log.objects.filter(upload_id=id).delete()
                            for upload_document in Uploades_documents.objects.filter(upload_id=id):

                                deleted = Document_attr_cross.objects.filter(document=upload_document.document).delete()
                                # logger.debug(f'deleted: {deleted}')

                                for item in Item.objects.filter(document=upload_document.document):
                                    Operations_item.objects.filter(item=item).delete()

                                    ItemManager.delete_recursive(item_id=item.id, delete_lines=True, user=user, props=0)
                                    # Ready_2_launch_detail.objects.filter(item=item).delete()
                                    item.delete()

                                for documents_history in Documents_history.objects.filter(new_document=upload_document.document):
                                    documents_history.old_document.props |= Documents.props.relevant
                                    documents_history.old_document.save()
                                    deleted = documents_history.delete()
                                    # logger.debug(f'deleted: {deleted}')

                                for thumb in Documents_thumb.objects.filter(document=upload_document.document):
                                    Item_image_refs.objects.filter(thumb=thumb).delete()
                                    deleted = thumb.delete()
                                    # logger.debug(f'deleted: {deleted}')

                                for thumb10 in Documents_thumb10.objects.filter(document=upload_document.document):
                                    Item_image_refs.objects.filter(thumb10=thumb10).delete()
                                    deleted = thumb10.delete()
                                    # logger.debug(f'deleted: {deleted}')

                                for lotsman_document in Lotsman_documents_hierarcy.objects.filter(document=upload_document.document):

                                    deleted = Lotsman_document_attr_cross.objects.filter(document=lotsman_document).delete()
                                    # logger.debug(f'deleted: {deleted}')
                                    deleted = Lotsman_document_attr_cross.objects.filter(parent_document=lotsman_document).delete()
                                    # logger.debug(f'deleted: {deleted}')
                                    deleted = Lotsman_documents_hierarcy_refs.objects.filter(child=lotsman_document).delete()
                                    # logger.debug(f'deleted: {deleted}')
                                    deleted = Lotsman_documents_hierarcy_refs.objects.filter(parent=lotsman_document).delete()
                                    # logger.debug(f'deleted: {deleted}')

                                    for thumb in Documents_thumb.objects.filter(lotsman_document=lotsman_document):
                                        Item_image_refs.objects.filter(thumb=thumb).delete()
                                        deleted = thumb.delete()
                                        # logger.debug(f'deleted: {deleted}')

                                    for thumb10 in Documents_thumb10.objects.filter(lotsman_document=lotsman_document):
                                        Item_image_refs.objects.filter(thumb10=thumb10).delete()
                                        deleted = thumb10.delete()
                                        # logger.debug(f'deleted: {deleted}')

                                    for item in Item.objects.filter(lotsman_document=lotsman_document):
                                        Operations_item.objects.filter(item=item).delete()

                                        ItemManager.delete_recursive(item_id=item.id, delete_lines=True, user=user, props=0)
                                        item.delete()

                                    Lotsman_documents_hierarcy_files.objects.filter(lotsman_document=lotsman_document).delete()
                                    deleted = lotsman_document.delete()
                                    # logger.debug(f'deleted: {deleted}')
                                    lotsman_cnt += 1
                                    res = progress.step()
                                    if res != 0:
                                        raise ProgressDroped(progress_deleted)

                                # logger.debug(f'Deliting: {upload_document.document}')
                                Documents.objects.filter(id=upload_document.document.id).delete()
                                # logger.debug(f'deleted: {deleted}')
                                Uploades_documents.objects.filter(upload_id=id).delete()
                                doc_cnt += 1
                                # logger.debug('Done.')
                                res = progress.step()
                                if res != 0:
                                    raise ProgressDroped(progress_deleted)

                            # logger.debug(f'deleted: {deleted}')

                            if doc_cnt > 0:
                                progress.setContentsLabel(blinkString(text='Обновление представления "kd_documents_mview"', color='blue'))
                                refresh_mat_view('kd_documents_mview')

                            if lotsman_cnt > 0:
                                progress.setContentsLabel(blinkString(text='Обновление представления "kd_lotsman_documents_hierarcy_mview"', color='blue'))
                                refresh_mat_view('kd_lotsman_documents_hierarcy_mview')

                            res += super().filter(id=id).delete()[0]
                    except ProgressDroped as ex:
                        Deleted_progresses.objects.filter(id_progress=progress.id, user=progress.user).delete()
                        raise ex
        return res


class Uploades(AuditModel):
    path = ForeignKeyCascade(Pathes)

    props = UploadesManager.props()

    objects = UploadesManager()

    def __str__(self):
        return f"{self.id}, path: [{self.path}]"

    class Meta:
        verbose_name = 'Загрузки внешних данных'
