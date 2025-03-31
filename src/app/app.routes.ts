import { RouterModule, Routes } from '@angular/router';
import { EtudiantComponent } from './etudiant/etudiant.component';
import { Component, NgModule } from '@angular/core';
import { ViewprofilComponent } from './etudiant/viewprofil/viewprofil.component';
import { UpdateStudentComponent } from './etudiant/update-student/update-student.component';
import { ScoreStudentComponent } from './etudiant/score-student/score-student.component';
import { AddstudentComponent } from './etudiant/addstudent/addstudent.component';
import { UploadStudentsComponent } from './etudiant/upload-students/upload-students.component';
import { SiteComponent } from './site/site.component';
import { PromotionComponent } from './promotion/promotion.component';
import { GroupeComponent } from './groupe/groupe.component';
import { AddGroupComponent } from './groupe/addgroupe/addgroup/addgroup.component';
import { UpdateGroupComponent } from './groupe/updategroupe/updategroup/updategroup.component';
import { AddPromoComponent } from './promotion/addPromo/add-promo/add-promo.component';
import { UpdatePromoComponent } from './promotion/updatePromo/update-promo/update-promo.component';

export const routes: Routes = [
    { path: 'studentlist', component: EtudiantComponent },
    { path: 'viewprofil/:id', component:ViewprofilComponent },
    {path:'update-student/:id', component:UpdateStudentComponent},
    {path: 'scorestudent/:id',component:ScoreStudentComponent},
    {path:'addstudent', component:AddstudentComponent},
    {path:'uploadstudent',component:UploadStudentsComponent},
    {path:'site',component:SiteComponent},
    {path:'promotionlist',component:PromotionComponent},
    {path:'groupelist',component:GroupeComponent},
    {path:'addgroup',component:AddGroupComponent},
    {path:'updategroup/:id',component:UpdateGroupComponent},
    {path:'scorestudent',component:ScoreStudentComponent},
    { path: 'addpromo', component:AddPromoComponent },
    { path: 'updatepromo/:id',component:UpdatePromoComponent  }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
