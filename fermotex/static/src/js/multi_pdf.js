odoo.define('fermotex.multi_pdf', function (require) {
"use strict";

var AbstractField = require('web.AbstractField');
var DocumentViewer = require('mail.DocumentViewer');
var core = require('web.core');
var data = require('web.data');
var fieldRegistry = require('web.field_registry');

var _t = core._t;
var qweb = core.qweb;

var MultiPDF = AbstractField.extend({
    template: "MultiPDF",
//    template_files: "FieldPdfViewer",
    template_files: "MultiPDF.files",
    supportedFieldTypes: ['many2many'],
    fieldsToFetch: {
        name: {type: 'char'},
        mimetype: {type: 'char'},
    },
    events: {
        'click .o_attach': '_onAttach',
        'click .o_attachment_delete': '_onDelete',
//        'click .o_attachment_download': '_onAttachmentDownload',
        'click .o_attachment_view': '_onAttachmentView',
//        'click .o_attachment_delete_cross': '_onDeleteAttachment',
        'change .o_input_file': '_onFileChanged',
    },
    /**
     * @constructor
     */
    init: function () {
        this._super.apply(this, arguments);

        if (this.field.type !== 'many2many' || this.field.relation !== 'ir.attachment') {
            var msg = _t("The type of the field '%s' must be a many2many field with a relation to 'ir.attachment' model.");
            throw _.str.sprintf(msg, this.field.string);
        }

        this.uploadedFiles = {};
        this.uploadingFiles = [];
        this.fileupload_id = _.uniqueId('oe_fileupload_temp');
        $(window).on(this.fileupload_id, this._onFileLoaded.bind(this));

        this.metadata = {};
    },

    destroy: function () {
        this._super();
        $(window).off(this.fileupload_id);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Compute the URL of an attachment.
     *
     * @private
     * @param {Object} attachment
     * @returns {string} URL of the attachment
     */
    _getFileUrl: function (attachment) {
        return '/web/content/' + attachment.id + '?download=true';
//        return "/web/content/" + attachment.id;
    },
    /**
     * Process the field data to add some information (url, etc.).
     *
     * @private
     */
    _generatedMetadata: function () {
        var self = this;
        _.each(this.value.data, function (record) {
            // tagging `allowUnlink` ascertains if the attachment was user
            // uploaded or was an existing or system generated attachment
            self.metadata[record.id] = {
                allowUnlink: self.uploadedFiles[record.data.id] || false,
                url: self._getFileUrl(record.data),
            };
        });
    },
    /**
     * @private
     * @override
     */
    _render: function () {
        // render the attachments ; as the attachments will changes after each
        // _setValue, we put the rendering here to ensure they will be updated
        this._generatedMetadata();
        this.$('.oe_placeholder_files, .o_attachments')
            .replaceWith($(qweb.render(this.template_files, {
                widget: this,
            })));
        this.$('.oe_fileupload').show();

        // display image thumbnail
        this.$('.o_image[data-mimetype^="image"]').each(function () {
            var $img = $(this);
            if (/gif|jpe|jpg|png/.test($img.data('mimetype')) && $img.data('src')) {
                $img.css('background-image', "url('" + $img.data('src') + "')");
            }
        });
    },
    _onAttachmentDownload: function(event) {
        event.stopPropagation();
    },
    _onAttachmentView: function(event) {
        event.stopPropagation();
        var attachments = _.uniq(_.flatten(_.map(this.value.data, function (message) {
            var data = message.data
            data.url = '/web/content/' + data.id + '?download=true'
            return data;
        })));
        var activeAttachmentID = $(event.currentTarget).data('id');
        if (activeAttachmentID) {
            var attachmentViewer = new DocumentViewer(this,attachments,activeAttachmentID);
            attachmentViewer.appendTo($('body'));
        }
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _onAttach: function () {
        // This widget uses a hidden form to upload files. Clicking on 'Attach'
        // will simulate a click on the related input.
        this.$('.o_input_file').click();
    },
    /**
     * @private
     * @param {MouseEvent} ev
     */
    _onDelete: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();

        var fileID = $(ev.currentTarget).data('id');
        var record = _.findWhere(this.value.data, {res_id: fileID});
        if (record) {
            this._setValue({
                operation: 'FORGET',
                ids: [record.id],
            });
            var metadata = this.metadata[record.id];
            if (!metadata || metadata.allowUnlink) {
                this._rpc({
                    model: 'ir.attachment',
                    method: 'unlink',
                    args: [record.res_id],
                });
            }
        }
    },
    /**
     * @private
     * @param {Event} ev
     */
    _onFileChanged: function (ev) {
        var self = this;
        ev.stopPropagation();

        var files = ev.target.files;
        var attachment_ids = this.value.res_ids;

        // Don't create an attachment if the upload window is cancelled.
        if(files.length === 0)
            return;

        _.each(files, function (file) {
            var record = _.find(self.value.data, function (attachment) {
                return attachment.data.name === file.name;
            });
            if (record) {
                var metadata = self.metadata[record.id];
                if (!metadata || metadata.allowUnlink) {
                    // there is a existing attachment with the same name so we
                    // replace it
                    attachment_ids = _.without(attachment_ids, record.res_id);
                    self._rpc({
                        model: 'ir.attachment',
                        method: 'unlink',
                        args: [record.res_id],
                    });
                }
            }
            self.uploadingFiles.push(file);
        });

        this._setValue({
            operation: 'REPLACE_WITH',
            ids: attachment_ids,
        });

        this.$('form.o_form_binary_form').submit();
        this.$('.oe_fileupload').hide();
        ev.target.value = "";
    },
    /**
     * @private
     */
    _onFileLoaded: function () {
        var self = this;
        // the first argument isn't a file but the jQuery.Event
        var files = Array.prototype.slice.call(arguments, 1);
        // files has been uploaded, clear uploading
        this.uploadingFiles = [];

        var attachment_ids = this.value.res_ids;
        _.each(files, function (file) {
            if (file.error) {
                self.do_warn(_t('Uploading Error'), file.error);
            } else {
                attachment_ids.push(file.id);
                self.uploadedFiles[file.id] = true;
            }
        });

        this._setValue({
            operation: 'REPLACE_WITH',
            ids: attachment_ids,
        });
    },
});

fieldRegistry.add('multi_pdf', MultiPDF);

return MultiPDF;

});
