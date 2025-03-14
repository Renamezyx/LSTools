<template>
    <el-table :data="tableData" style="width: 100%" max-height="600">
        <el-table-column fixed prop="date" label="Date" width="150" sortable />
        <el-table-column prop="name" label="Name" width="120" />
        <el-table-column prop="stats" label="Stats" width="120" sortable>
            <template #default="scope">
                <el-tag type="primary" effect="light" v-if="scope.row.stats == 0">{{ stats_format(scope.row.stats)
                }}</el-tag>
                <el-tag type="success" effect="light" v-if="scope.row.stats == 1">{{ stats_format(scope.row.stats)
                }}</el-tag>
                <el-tag type="danger" effect="light" v-if="scope.row.stats == -1">{{ stats_format(scope.row.stats)
                }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column prop="account" label="Account" width="120" />
        <el-table-column prop="cookies" label="Cookies" width="600" show-overflow-tooltip />
        <el-table-column fixed="right" label="Operations" min-width="220">
            <template #default="scope">
                <el-button link type="primary" size="small" @click.prevent="push(scope.row.id)">
                    Push
                </el-button>
                <el-button link type="info" size="small" @click.prevent="edit(scope.row.id)">
                    Edit
                </el-button>
                <el-button link type="danger" size="small" @click.prevent="del(scope.row.id)">
                    Remove
                </el-button>
            </template>
        </el-table-column>
    </el-table>
    <el-button class="mt-4" style="width: 100%" @click="openDrawer('add')">
        Add Item
    </el-button>
    <el-drawer v-model="drawer" title="Input" :direction="direction" :before-close="handleClose">
        <el-form label-width="100px">
            <el-form-item label="UserName">
                <el-input v-model="User.username" style="width: 240px" placeholder="Please input your username"
                    clearable />
            </el-form-item>

            <el-form-item label="Phone">
                <el-input v-model="User.phone" style="width: 240px" placeholder="Please input your phone number"
                    clearable />
            </el-form-item>

            <el-form-item label="Headers">
                <el-input v-model="User.headers" style="width: 240px" :autosize="{ minRows: 2, maxRows: 4 }"
                    type="textarea" placeholder="Please input your headers" />
            </el-form-item>
        </el-form>
        <template #footer>
            <div style="flex: auto">
                <el-button @click="cancelClick">cancel</el-button>
                <el-button type="primary" @click="confirmClick">confirm</el-button>
            </div>
        </template>
    </el-drawer>

</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue'
import type { DrawerProps } from 'element-plus'
import { ElMessageBox } from 'element-plus'
import service from '@/utils/request'

const User = reactive({
    "username": "",
    "phone": "",
    "headers": ""
})

const drawer = ref(false)
const direction = ref<DrawerProps['direction']>('rtl')
const now = new Date()

const tableData = ref([
    {
        id: 1,
        date: '2016-05-01',
        name: 'Tom',
        account: '123',
        cookies: "store-idc=alisg; store-country-code=tr; store-country-code-src=uid; tt-target-idc=alisg; ttwid=1%7Cjn0Z-4oixOAZ_WXnC-wA3h6gDEZ2plPvm7FYfnfp6EA%7C1740486446%7Cdd10046bc1c2e4a0dda06ce8dc39c3ca5ad2096348c32aa7fc284572d7300b2a; d_ticket=d7041ca64c8999f5ffaae8801c283e5b8b65d; multi_sids=7200686585301402630%3A019d7373b13a6393f650b10afce9d79d; cmpl_token=AgQQAPOGF-RO0rPTFOvv_V0__dwv50EU_4o3YNk4Hw; passport_auth_status=93d2762145c7c1110307b5f2c791dcc3%2C; passport_auth_status_ss=93d2762145c7c1110307b5f2c791dcc3%2C; tt_chain_token=eyDdpV8htoK/qW4KKesKWw==; passport_csrf_token=eaf8b12c16a52a8722ee5f1db40e3fb2; passport_csrf_token_default=eaf8b12c16a52a8722ee5f1db40e3fb2; sid_guard=7b8d0fa81c2b8a7cfdbafda8aa749020%7C1740486464%7C5184000%7CSat%2C+26-Apr-2025+12%3A27%3A44+GMT; uid_tt=82e48af5e2a1bd1bca5b5ac6ec1f5f5ef55a37c7c8a4c2ece667d8b835671b6c; uid_tt_ss=82e48af5e2a1bd1bca5b5ac6ec1f5f5ef55a37c7c8a4c2ece667d8b835671b6c; sid_tt=7b8d0fa81c2b8a7cfdbafda8aa749020; sessionid=7b8d0fa81c2b8a7cfdbafda8aa749020; sessionid_ss=7b8d0fa81c2b8a7cfdbafda8aa749020; sid_ucp_v1=1.0.0-KGVkYzlhNjQ3MjNlY2I1ZTA0NjBjZGY3YmViMjIzN2U4YzI5NTE2MzEKGAiGiL6-xsn-9mMQwO72vQYY90A4BkCACBADGgNzZzEiIDdiOGQwZmE4MWMyYjhhN2NmZGJhZmRhOGFhNzQ5MDIw; ssid_ucp_v1=1.0.0-KGVkYzlhNjQ3MjNlY2I1ZTA0NjBjZGY3YmViMjIzN2U4YzI5NTE2MzEKGAiGiL6-xsn-9mMQwO72vQYY90A4BkCACBADGgNzZzEiIDdiOGQwZmE4MWMyYjhhN2NmZGJhZmRhOGFhNzQ5MDIw; tt-target-idc-sign=Twg9kgEJ_NxaqOW3BgBO_5oN_7kXMtoeH7Gua_2YO-8SXb4IFx97mZCplGoHhIsVLFGIVmSwaBY6uvRSYtvrjJH2XF-wsXuOfNV-oxE6nKTn2avjTV_QLe8T0ZsCjIbBtQMVny91MK-B_xHARTZJvMxHlo1Pu3QXl1eS6sMlASfTlv9H5BVlDXH4Dcw52hqazMvsMBtGRR3KAeC4XiUxVmxZZgAuY1UlkwWtxD8zAAPA_vHNEgpLGDuykR55nEdQQDugGm8SsH2mXc4M9slDunY0XDLcw1dHp93KwSyH1LnLYT4z1im5Pwb5uQVkOzmyQhZ87Q1LMYPKGIaIH2W0nTYEHF_wCUgviRv5Ah4wKS-wwru40y_KwxcDjCAjTX6NIYD6F8QQGoI37RHIRiYViZk1KPIZc8poSAfq5VW39VpCBJJ7CWmJd-i2R9GhBz0aRJjyJkHRVadmDPJk2zRAJkbgpREhHnpXSt12sMg9vArRDzv5TsQk2KgkZ55nxVTt; odin_tt=1dfdfe8d60f9e52c919153765359b3d3e172ed66431451e9ef4ccfd49942ad0a2a3d8f97e2874c2cfd5f843a94f15607daee9439461f89ad2bf3d61f06d712b6c0a1f14cab8be4c2d49111c606c8ae6d; msToken=In5J17PMZIsKPCvwadwffFFW-r66k21XHCegTHDQI2UU_0zjKTuRoRFtmFfDj75ZSDoVVB2DwglXc7esF5R2oyQXOqRv5HsrAUl4OEw9Jlab",
        stats: 0
    },
    {
        id: 2,
        date: '2016-05-02',
        name: 'Tom',
        account: '123',
        cookies: "store-idc=alisg; store-country-code=tr; store-country-code-src=uid; tt-target-idc=alisg; ttwid=1%7Cjn0Z-4oixOAZ_WXnC-wA3h6gDEZ2plPvm7FYfnfp6EA%7C1740486446%7Cdd10046bc1c2e4a0dda06ce8dc39c3ca5ad2096348c32aa7fc284572d7300b2a; d_ticket=d7041ca64c8999f5ffaae8801c283e5b8b65d; multi_sids=7200686585301402630%3A019d7373b13a6393f650b10afce9d79d; cmpl_token=AgQQAPOGF-RO0rPTFOvv_V0__dwv50EU_4o3YNk4Hw; passport_auth_status=93d2762145c7c1110307b5f2c791dcc3%2C; passport_auth_status_ss=93d2762145c7c1110307b5f2c791dcc3%2C; tt_chain_token=eyDdpV8htoK/qW4KKesKWw==; passport_csrf_token=eaf8b12c16a52a8722ee5f1db40e3fb2; passport_csrf_token_default=eaf8b12c16a52a8722ee5f1db40e3fb2; sid_guard=7b8d0fa81c2b8a7cfdbafda8aa749020%7C1740486464%7C5184000%7CSat%2C+26-Apr-2025+12%3A27%3A44+GMT; uid_tt=82e48af5e2a1bd1bca5b5ac6ec1f5f5ef55a37c7c8a4c2ece667d8b835671b6c; uid_tt_ss=82e48af5e2a1bd1bca5b5ac6ec1f5f5ef55a37c7c8a4c2ece667d8b835671b6c; sid_tt=7b8d0fa81c2b8a7cfdbafda8aa749020; sessionid=7b8d0fa81c2b8a7cfdbafda8aa749020; sessionid_ss=7b8d0fa81c2b8a7cfdbafda8aa749020; sid_ucp_v1=1.0.0-KGVkYzlhNjQ3MjNlY2I1ZTA0NjBjZGY3YmViMjIzN2U4YzI5NTE2MzEKGAiGiL6-xsn-9mMQwO72vQYY90A4BkCACBADGgNzZzEiIDdiOGQwZmE4MWMyYjhhN2NmZGJhZmRhOGFhNzQ5MDIw; ssid_ucp_v1=1.0.0-KGVkYzlhNjQ3MjNlY2I1ZTA0NjBjZGY3YmViMjIzN2U4YzI5NTE2MzEKGAiGiL6-xsn-9mMQwO72vQYY90A4BkCACBADGgNzZzEiIDdiOGQwZmE4MWMyYjhhN2NmZGJhZmRhOGFhNzQ5MDIw; tt-target-idc-sign=Twg9kgEJ_NxaqOW3BgBO_5oN_7kXMtoeH7Gua_2YO-8SXb4IFx97mZCplGoHhIsVLFGIVmSwaBY6uvRSYtvrjJH2XF-wsXuOfNV-oxE6nKTn2avjTV_QLe8T0ZsCjIbBtQMVny91MK-B_xHARTZJvMxHlo1Pu3QXl1eS6sMlASfTlv9H5BVlDXH4Dcw52hqazMvsMBtGRR3KAeC4XiUxVmxZZgAuY1UlkwWtxD8zAAPA_vHNEgpLGDuykR55nEdQQDugGm8SsH2mXc4M9slDunY0XDLcw1dHp93KwSyH1LnLYT4z1im5Pwb5uQVkOzmyQhZ87Q1LMYPKGIaIH2W0nTYEHF_wCUgviRv5Ah4wKS-wwru40y_KwxcDjCAjTX6NIYD6F8QQGoI37RHIRiYViZk1KPIZc8poSAfq5VW39VpCBJJ7CWmJd-i2R9GhBz0aRJjyJkHRVadmDPJk2zRAJkbgpREhHnpXSt12sMg9vArRDzv5TsQk2KgkZ55nxVTt; odin_tt=1dfdfe8d60f9e52c919153765359b3d3e172ed66431451e9ef4ccfd49942ad0a2a3d8f97e2874c2cfd5f843a94f15607daee9439461f89ad2bf3d61f06d712b6c0a1f14cab8be4c2d49111c606c8ae6d; msToken=In5J17PMZIsKPCvwadwffFFW-r66k21XHCegTHDQI2UU_0zjKTuRoRFtmFfDj75ZSDoVVB2DwglXc7esF5R2oyQXOqRv5HsrAUl4OEw9Jlab",
        stats: 0
    },
    {
        id: 3,
        date: '2016-05-03',
        name: 'Tom',
        account: '123',
        cookies: "store-idc=alisg; store-country-code=tr; store-country-code-src=uid; tt-target-idc=alisg; ttwid=1%7Cjn0Z-4oixOAZ_WXnC-wA3h6gDEZ2plPvm7FYfnfp6EA%7C1740486446%7Cdd10046bc1c2e4a0dda06ce8dc39c3ca5ad2096348c32aa7fc284572d7300b2a; d_ticket=d7041ca64c8999f5ffaae8801c283e5b8b65d; multi_sids=7200686585301402630%3A019d7373b13a6393f650b10afce9d79d; cmpl_token=AgQQAPOGF-RO0rPTFOvv_V0__dwv50EU_4o3YNk4Hw; passport_auth_status=93d2762145c7c1110307b5f2c791dcc3%2C; passport_auth_status_ss=93d2762145c7c1110307b5f2c791dcc3%2C; tt_chain_token=eyDdpV8htoK/qW4KKesKWw==; passport_csrf_token=eaf8b12c16a52a8722ee5f1db40e3fb2; passport_csrf_token_default=eaf8b12c16a52a8722ee5f1db40e3fb2; sid_guard=7b8d0fa81c2b8a7cfdbafda8aa749020%7C1740486464%7C5184000%7CSat%2C+26-Apr-2025+12%3A27%3A44+GMT; uid_tt=82e48af5e2a1bd1bca5b5ac6ec1f5f5ef55a37c7c8a4c2ece667d8b835671b6c; uid_tt_ss=82e48af5e2a1bd1bca5b5ac6ec1f5f5ef55a37c7c8a4c2ece667d8b835671b6c; sid_tt=7b8d0fa81c2b8a7cfdbafda8aa749020; sessionid=7b8d0fa81c2b8a7cfdbafda8aa749020; sessionid_ss=7b8d0fa81c2b8a7cfdbafda8aa749020; sid_ucp_v1=1.0.0-KGVkYzlhNjQ3MjNlY2I1ZTA0NjBjZGY3YmViMjIzN2U4YzI5NTE2MzEKGAiGiL6-xsn-9mMQwO72vQYY90A4BkCACBADGgNzZzEiIDdiOGQwZmE4MWMyYjhhN2NmZGJhZmRhOGFhNzQ5MDIw; ssid_ucp_v1=1.0.0-KGVkYzlhNjQ3MjNlY2I1ZTA0NjBjZGY3YmViMjIzN2U4YzI5NTE2MzEKGAiGiL6-xsn-9mMQwO72vQYY90A4BkCACBADGgNzZzEiIDdiOGQwZmE4MWMyYjhhN2NmZGJhZmRhOGFhNzQ5MDIw; tt-target-idc-sign=Twg9kgEJ_NxaqOW3BgBO_5oN_7kXMtoeH7Gua_2YO-8SXb4IFx97mZCplGoHhIsVLFGIVmSwaBY6uvRSYtvrjJH2XF-wsXuOfNV-oxE6nKTn2avjTV_QLe8T0ZsCjIbBtQMVny91MK-B_xHARTZJvMxHlo1Pu3QXl1eS6sMlASfTlv9H5BVlDXH4Dcw52hqazMvsMBtGRR3KAeC4XiUxVmxZZgAuY1UlkwWtxD8zAAPA_vHNEgpLGDuykR55nEdQQDugGm8SsH2mXc4M9slDunY0XDLcw1dHp93KwSyH1LnLYT4z1im5Pwb5uQVkOzmyQhZ87Q1LMYPKGIaIH2W0nTYEHF_wCUgviRv5Ah4wKS-wwru40y_KwxcDjCAjTX6NIYD6F8QQGoI37RHIRiYViZk1KPIZc8poSAfq5VW39VpCBJJ7CWmJd-i2R9GhBz0aRJjyJkHRVadmDPJk2zRAJkbgpREhHnpXSt12sMg9vArRDzv5TsQk2KgkZ55nxVTt; odin_tt=1dfdfe8d60f9e52c919153765359b3d3e172ed66431451e9ef4ccfd49942ad0a2a3d8f97e2874c2cfd5f843a94f15607daee9439461f89ad2bf3d61f06d712b6c0a1f14cab8be4c2d49111c606c8ae6d; msToken=In5J17PMZIsKPCvwadwffFFW-r66k21XHCegTHDQI2UU_0zjKTuRoRFtmFfDj75ZSDoVVB2DwglXc7esF5R2oyQXOqRv5HsrAUl4OEw9Jlab",
        stats: 1
    },
])

const push = (id: number) => {
    console.log("push")
    console.log(id)
}

const edit = (index: number) => {
    console.log("edit")
}
const del = (index: number) => {
    console.log("del")
}

const openDrawer = (type: string) => {
    if (type == "add") {
        User.username = ""
        User.phone = ""
        User.headers = ""
    }
    drawer.value = true

}

const stats_format = (stats: number) => {
    switch (stats) {
        case 0:
            return "空闲"
        case 1:
            return "直播中"
        case -1:
            return "cookies过期"
        default:
            return "未知"
    }
}

const handleClose = (done: () => void) => {
    ElMessageBox.confirm('Are you sure you want to close this?')
        .then(() => {
            done()
        })
        .catch(() => {
            // catch error
        })
}

const cancelClick = () => {
    drawer.value = false
    console.log("cancel")
}

const confirmClick = async () => {
    console.log("confirm")

    try {
        const response = await service.post('/users/insert', {
            username: User.username,
            phone: User.phone,
            headers: User.headers
        })
        console.log('Response:', response)

        // 只有请求成功后，才关闭抽屉
        drawer.value = false  
    } catch (error) {
        console.error('Request failed:', error)
    }
}

</script>

<style scoped></style>