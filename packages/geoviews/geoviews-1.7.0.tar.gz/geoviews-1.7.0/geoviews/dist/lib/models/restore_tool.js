"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var p = require("@bokehjs/core/properties");
var action_tool_1 = require("@bokehjs/models/tools/actions/action_tool");
var RestoreToolView = /** @class */ (function (_super) {
    __extends(RestoreToolView, _super);
    function RestoreToolView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RestoreToolView.prototype.doit = function () {
        var sources = this.model.sources;
        for (var _i = 0, sources_1 = sources; _i < sources_1.length; _i++) {
            var source = sources_1[_i];
            if (!source.buffer || (source.buffer.length == 0)) {
                continue;
            }
            source.data = source.buffer.pop();
            source.change.emit();
            source.properties.data.change.emit();
        }
    };
    RestoreToolView.__name__ = "RestoreToolView";
    return RestoreToolView;
}(action_tool_1.ActionToolView));
exports.RestoreToolView = RestoreToolView;
var RestoreTool = /** @class */ (function (_super) {
    __extends(RestoreTool, _super);
    function RestoreTool(attrs) {
        var _this = _super.call(this, attrs) || this;
        _this.tool_name = "Restore";
        _this.icon = "bk-tool-icon-undo";
        return _this;
    }
    RestoreTool.init_RestoreTool = function () {
        this.prototype.default_view = RestoreToolView;
        this.define({
            sources: [p.Array, []]
        });
    };
    RestoreTool.__name__ = "RestoreTool";
    RestoreTool.__module__ = "geoviews.models.custom_tools";
    return RestoreTool;
}(action_tool_1.ActionTool));
exports.RestoreTool = RestoreTool;
RestoreTool.init_RestoreTool();
//# sourceMappingURL=restore_tool.js.map