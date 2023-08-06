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
var ClearToolView = /** @class */ (function (_super) {
    __extends(ClearToolView, _super);
    function ClearToolView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ClearToolView.prototype.doit = function () {
        for (var _i = 0, _a = this.model.sources; _i < _a.length; _i++) {
            var source = _a[_i];
            for (var column in source.data) {
                source.data[column] = [];
            }
            source.change.emit();
            source.properties.data.change.emit();
        }
    };
    ClearToolView.__name__ = "ClearToolView";
    return ClearToolView;
}(action_tool_1.ActionToolView));
exports.ClearToolView = ClearToolView;
var ClearTool = /** @class */ (function (_super) {
    __extends(ClearTool, _super);
    function ClearTool(attrs) {
        var _this = _super.call(this, attrs) || this;
        _this.tool_name = "Clear data";
        _this.icon = "bk-tool-icon-reset";
        return _this;
    }
    ClearTool.init_ClearTool = function () {
        this.prototype.type = "ClearTool";
        this.prototype.default_view = ClearToolView;
        this.define({
            sources: [p.Array, []],
        });
    };
    ClearTool.__name__ = "ClearTool";
    ClearTool.__module__ = "geoviews.models.custom_tools";
    return ClearTool;
}(action_tool_1.ActionTool));
exports.ClearTool = ClearTool;
ClearTool.init_ClearTool();
//# sourceMappingURL=clear_tool.js.map