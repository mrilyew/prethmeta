from representations.WebServices_Vk.BaseVk import BaseVkItemId
from declarable.ArgumentsTypes import BooleanArgument
from submodules.Web.DownloadManager import download_manager
from utils.MainUtils import entity_sign
from pathlib import Path
from app.App import logger
import os

class VkLink(BaseVkItemId):
    @classmethod
    def declare(cls):
        params = {}
        params["download"] = BooleanArgument({
            "default": True
        })

        return params

    class Extractor(BaseVkItemId.Extractor):
        def __response(self, i = {}):
            raise Exception('undefined')

        async def item(self, item, list_to_add):
            self.outer._insertVkLink(item, self.args.get('vk_path'))

            attached_photo = item.get("photo")
            should_be_unlisted = self.args.get('unlisted') == 1
            su = None

            logger.log(message=f"Recieved attached link",section="VkEntity",kind="message")

            if self.args.get("download") == True:
                if attached_photo != None:
                    photo_id = f"{attached_photo.get('owner_id')}_{attached_photo.get('id')}"
                    save_name = f"link_photo_{photo_id}.jpg"

                    try:
                        su = self.storageUnit()
                        temp_dir = su.temp_dir

                        __photo_sizes = sorted(attached_photo.get("sizes"), key=lambda x: (x['width'] is None, x['width']), reverse=True)
                        __optimal_size = __photo_sizes[0]

                        save_path = Path(os.path.join(temp_dir, save_name))

                        await download_manager.addDownload(end=__optimal_size.get("url"),dir=save_path)

                        file_size = save_path.stat().st_size

                        su.write_data({
                            "extension": "jpg",
                            "upload_name": save_name,
                            "filesize": file_size,
                        })

                        item['relative_photo'] = entity_sign(su)

                        logger.log(message=f"Downloaded link's photo {file_size}",section="VkEntity",kind="success")
                    except FileNotFoundError as _ea:
                        logger.log(message=f"Photo's file cannot be found. Probaly broken file? Exception: {str(_ea)}",section="VkEntity",kind="error")

            cu = self.contentUnit({
                "content": item,
                "source": {
                    "type": 'url',
                    "content": item.get('url')
                },
                "unlisted": should_be_unlisted,
                "name": f"Vk Attached link",
                "links": [su]
            })

            list_to_add.append(cu)
