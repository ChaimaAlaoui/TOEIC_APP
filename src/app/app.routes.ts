import { RouterModule, Routes } from '@angular/router';
import { EtudiantComponent } from './etudiant/etudiant.component';
import { NgModule } from '@angular/core';
import { ViewprofilComponent } from './etudiant/viewprofil/viewprofil.component';
import { UpdateStudentComponent } from './etudiant/update-student/update-student.component';
import { ScoreStudentComponent } from './etudiant/score-student/score-student.component';
import { AddstudentComponent } from './etudiant/addstudent/addstudent.component';
import { UploadStudentsComponent } from './etudiant/upload-students/upload-students.component';
import { SiteComponent } from './site/site.component';
import { PromotionComponent } from './promotion/promotion.component';
import { GroupeComponent } from './groupe/groupe.component';

export const routes: Routes = [
    { path: 'studentlist', component: EtudiantComponent },
    { path: 'viewprofil/:id', component:ViewprofilComponent },
    {path:'update-student/:id', component:UpdateStudentComponent},
    {path: 'scorestudent/:id',component:ScoreStudentComponent},
    {path:'addstudent', component:AddstudentComponent},
    {path:'uploadstudent',component:UploadStudentsComponent},
    {path:'site',component:SiteComponent},
    {path:'promotionlist',component:PromotionComponent},
    {path:'groupelist',component:GroupeComponent}
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
