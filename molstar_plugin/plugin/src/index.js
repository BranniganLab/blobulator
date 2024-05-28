"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
var spec_1 = require("../node_modules/molstar/lib/mol-plugin-ui/spec");
var mol_plugin_ui_1 = require("../node_modules/molstar/lib/mol-plugin-ui");
var react18_1 = require("../node_modules/molstar/lib/mol-plugin-ui/react18");
var config_1 = require("../node_modules/molstar/lib/mol-plugin/config");
var builder_1 = require("../node_modules/molstar/lib/mol-script/language/builder");
var color_1 = require("../node_modules/molstar/lib/mol-util/color");
var transforms_1 = require("../node_modules/molstar/lib/mol-plugin-state/transforms");
var structure_representation_params_1 = require("../node_modules/molstar/lib/mol-plugin-state/helpers/structure-representation-params");
var MySpec = __assign(__assign({}, (0, spec_1.DefaultPluginUISpec)()), { config: [
        [config_1.PluginConfig.VolumeStreaming.Enabled, false]
    ] });
function createPlugin(parent) {
    return __awaiter(this, void 0, void 0, function () {
        var plugin, data, trajectory, model, structure, components, builder, update, sel;
        var _a;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, (0, mol_plugin_ui_1.createPluginUI)({
                        target: parent,
                        spec: MySpec,
                        render: react18_1.renderReact18
                    })];
                case 1:
                    plugin = _b.sent();
                    return [4 /*yield*/, plugin.builders.data.download({ url: "https://files.rcsb.org/download/1dpx.pdb" }, { state: { isGhost: true } })];
                case 2:
                    data = _b.sent();
                    return [4 /*yield*/, plugin.builders.structure.parseTrajectory(data, 'pdb')];
                case 3:
                    trajectory = _b.sent();
                    return [4 /*yield*/, plugin.builders.structure.createModel(trajectory)];
                case 4:
                    model = _b.sent();
                    return [4 /*yield*/, plugin.builders.structure.createStructure(model)];
                case 5:
                    structure = _b.sent();
                    _a = {};
                    return [4 /*yield*/, plugin.builders.structure.tryCreateComponentStatic(structure, 'polymer')];
                case 6:
                    components = (_a.polymer = _b.sent(),
                        _a);
                    builder = plugin.builders.structure.representation;
                    update = plugin.build();
                    // // Select residue 124 of chain A and convert to Loci
                    // const Q = MolScriptBuilder;
                    // var sel = Script.getStructureSelection(Q => Q.struct.generator.atomGroups({
                    //                 "residue-test": Q.core.rel.eq([Q.struct.atomProperty.macromolecular.label_seq_id(), 11]),
                    //               }), objdata)
                    // const components = {
                    //     blob: await plugin.builders.structure.tryCreateComponentFromSelection(structure, sel, "residue-test")
                    // }
                    // builder.buildRepresentation(update, components.polymer, { type: 'gaussian-surface', typeParams: { alpha: 0.51 }, color : 'uniform', colorParams: { value: Color(0x073763) } }, { tag: 'polymer' });
                    builder.buildRepresentation(update, components.polymer, { type: 'cartoon', typeParams: { alpha: 1.0 }, color: 'uniform', colorParams: { value: (0, color_1.Color)(0xFFA500) } }, { tag: 'polymer' });
                    sel = builder_1.MolScriptBuilder.struct.generator.atomGroups({
                        'residue-test': builder_1.MolScriptBuilder.core.rel.eq([builder_1.MolScriptBuilder.struct.atomProperty.macromolecular.label_seq_id(), '1-15']),
                    });
                    update.to(structure)
                        .apply(transforms_1.StateTransforms.Model.StructureSelectionFromExpression, { label: 'Surroundings', expression: sel })
                        .apply(transforms_1.StateTransforms.Representation.StructureRepresentation3D, (0, structure_representation_params_1.createStructureRepresentationParams)(plugin, structure.data, {
                        type: 'gaussian-surface',
                        color: 'uniform',
                        colorParams: { value: (0, color_1.Color)(0x0096FF) }
                    }));
                    return [4 /*yield*/, update.commit()];
                case 7:
                    _b.sent();
                    return [2 /*return*/, plugin];
            }
        });
    });
}
createPlugin(document.getElementById('app')); // app is a <div> element with position: relative
