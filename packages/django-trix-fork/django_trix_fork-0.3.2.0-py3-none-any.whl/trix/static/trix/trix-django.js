(function() {
    addEventListener("trix-attachment-add", function(event) {
        if (event.attachment.file) {
            uploadFileAttachment(event.attachment)
        }
    })

    function uploadFileAttachment(attachment) {
        uploadFile(attachment.file, setProgress, setAttributes)

        function setProgress(progress) {
          attachment.setUploadProgress(progress)
        }

        function setAttributes(attributes) {
          attachment.setAttributes(attributes)
        }
    }

    function uploadFile(file, progressCallback, successCallback) {
        var key = createStorageKey(file)
        var formData = createFormData(key, file)
        var xhr = new XMLHttpRequest()

        xhr.open("POST", '/trix/attachment/', true)

        xhr.upload.addEventListener("progress", function(event) {
            var progress = event.loaded / event.total * 100
            progressCallback(progress)
        })

        xhr.addEventListener("load", function(event) {
            if (xhr.status == 200) {
                resp = JSON.parse(xhr.response)
                if (resp.valid === 'true') {
                    media_url = resp.url
                    var attributes = {
                        url: media_url ,
                        href: media_url + "?content-disposition=attachment"
                    }
                    successCallback(attributes)
                } else {
                    alert(`File Upload Failed: ${resp.msg}`);
                }
            } else {
                alert(`Error ${xhr.status}: ${xhr.statusText}`);
            }
        })

        xhr.send(formData)
    }
    function createStorageKey(file) {
        var date = new Date()
        var day = date.toISOString().slice(0,10)
        var name = date.getTime() + "-" + file.name
        return [ day, name ].join("_")
    }

    function createFormData(key, file) {
        var data = new FormData()
        data.append("title", key)
        data.append("Content-Type", file.type)
        data.append("file", file)
        return data
    }
})();