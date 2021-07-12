<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 权限管理
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-button type="primary" icon="el-icon-plus" class="add_button"  size='medium'
            @click="addScene">添加权限</el-button>
            <el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
                <el-table-column prop="id" label="ID" width="55" align="center"></el-table-column>
                <el-table-column prop="name" label="权限名称"></el-table-column>
                <el-table-column prop="role" label="使用角色"></el-table-column>
                <el-table-column prop="scope" label="权限范围"></el-table-column>
                <el-table-column prop="createPeo" label="创建者"></el-table-column>
                <el-table-column prop="date" label="创建时间"></el-table-column>
                <el-table-column label="操作" width="180" align="center">
                    <template #default="scope">
                        <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.$index, scope.row)">编辑
                        </el-button>
                        <el-button type="text" icon="el-icon-delete" class="red"
                            @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="pagination">
                <el-pagination background layout="total, prev, pager, next" :current-page="query.pageIndex"
                    :page-size="query.pageSize" :total="pageTotal" @current-change="handlePageChange"></el-pagination>
            </div>
        </div>
        <!-- 编辑弹出框 -->
        <el-dialog title="编辑" v-model="editVisible" width="30%">
            <el-form label-width="70px">
                <el-form-item label="权限名称">
                    <el-input v-model="form.name"></el-input>
                </el-form-item>
                <el-form-item label="使用角色">
                    <el-input v-model="form.role"></el-input>
                </el-form-item>
                <el-form-item label="权限范围">
                    <el-input v-model="form.scope"></el-input>
                </el-form-item>
                <el-form-item label="创建者">
                    <el-input v-model="form.createPeo"></el-input>
                </el-form-item>
                <el-form-item label="创建时间">
                    <el-input v-model="form.date"></el-input>
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="editVisible = false">取 消</el-button>
                    <el-button type="primary" @click="saveEdit">确 定</el-button>
                </span>
            </template>
        </el-dialog>
        <!-- 添加弹出框 -->
        <el-dialog title="添加" v-model="addVisible" width="30%">
            <el-form label-width="100px" label-position="left">
                <el-form-item label="权限名称" class="label_big">
                    <el-input v-model="newForm.name"></el-input>
                </el-form-item>
                <el-form-item label="可使用角色" class="label_big">
                    <el-checkbox-group v-model="newForm.role">
                        <el-checkbox label="管理员" name="1"></el-checkbox>
                        <el-checkbox label="普通员工" name="2"></el-checkbox>
                        <el-checkbox label="领导人" name="3"></el-checkbox>
                        <el-checkbox label="干事" name="4"></el-checkbox>
                      </el-checkbox-group>
                </el-form-item>
                <el-form-item label="权限管理范围" class="label_big">
                    <el-input v-model="newForm.scope"></el-input>
                </el-form-item>
            </el-form>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="addVisible = false">取 消</el-button>
                    <el-button type="primary" @click="saveAdd">确 定</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script>
import { ref, reactive } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { fetchData } from "../api/index";

export default {
    name: "basetable",
    setup() {
        const query = reactive({
            role: "",
            name: "",
            pageIndex: 1,
            pageSize: 10,
            scene:"",
        });
        // 新加的数据
        const addVisible = ref(false);
        const newForm = reactive({
            name:"",
            role:[],
            scope:"",
        })
        const addScene = ()=>{
            addVisible.value=true
        }
        const saveAdd = ()=>{
            addVisible.value=false

            // 清空
            console.log(newForm.name)
            Object.keys(newForm).forEach((item) => {
                newForm[item] = "";
            });
        }

        const tableData = ref([]);
        const pageTotal = ref(0);
        // 获取表格数据
        const getData = () => {
            fetchData(query).then((res) => {
                tableData.value = res.list;
                pageTotal.value = res.pageTotal || 50;
            });
        };
        getData();

        // 查询操作
        const handleSearch = () => {
            query.pageIndex = 1;
            getData();
        };
        // 分页导航
        const handlePageChange = (val) => {
            query.pageIndex = val;
            getData();
        };

        // 删除操作
        const handleDelete = (index) => {
            // 二次确认删除
            ElMessageBox.confirm("确定要删除吗？", "提示", {
                type: "warning",
            })
                .then(() => {
                    ElMessage.success("删除成功");
                    tableData.value.splice(index, 1);
                })
                .catch(() => {});
        };

        // 表格编辑时弹窗和保存
        const editVisible = ref(false);
        let form = reactive({
            name: "",
            role:"",
            scope:"",
            createPeo:"",
            date:"",
        });
        let idx = -1;
        const handleEdit = (index, row) => {
            idx = index;
            Object.keys(form).forEach((item) => {
                form[item] = row[item];
            });
            editVisible.value = true;
        };
        const saveEdit = () => {
            editVisible.value = false;
            ElMessage.success(`修改第 ${idx + 1} 行成功`);
            Object.keys(form).forEach((item) => {
                tableData.value[idx][item] = form[item];
            });
        };

        return {
            query,
            tableData,
            pageTotal,
            editVisible,
            form,
            handleSearch,
            handlePageChange,
            handleDelete,
            handleEdit,
            saveEdit,
            addScene,
            saveAdd,
            newForm,
            addVisible,
        };
    },
};
</script>

<style scoped>

.add_button{
    margin-bottom: 20px;
}

.handle-box {
    margin-bottom: 20px;
}

.handle-select {
    width: 120px;
}

.handle-input {
    width: 300px;
    display: inline-block;
}
.table {
    width: 100%;
    font-size: 14px;
}
.red {
    color: #ff0000;
}
.mr10 {
    margin-right: 10px;
}
.table-td-thumb {
    display: block;
    margin: auto;
    width: 40px;
    height: 40px;
}
</style>
