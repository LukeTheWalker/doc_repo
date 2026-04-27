---
title: "Vector Identities"
nav_order: 3
parent: "Physics Models"
layout: default
render_with_liquid: false
---

# Appendix: Vector Identities

For arbitrary scalars $a$ and vectors $\mathbf{A}, \mathbf{B}, \mathbf{C}, \mathbf{D}$:
$$\begin{align}
\mathbf{A}\times\mathbf{A}&=0 \\
\nabla\cdot\nabla\times\mathbf{A} &= 0 \\
\nabla\times\nabla a &= 0 \\
\mathbf{A}\cdot(\mathbf{A}\times\mathbf{B}) &= 0 \\
\mathbf{A}\cdot\mathbf{B} &= \mathbf{B}\cdot\mathbf{A} \\
\mathbf{A}\times\mathbf{B} &= - \mathbf{B}\times\mathbf{A} \\
\mathbf{A}\cdot(\mathbf{B}\times\mathbf{C}) &= -\mathbf{B}\cdot(\mathbf{A}\times\mathbf{C}) = -\mathbf{C}\cdot(\mathbf{B}\times\mathbf{A})\\
\mathbf{A}\times(\mathbf{B}\times\mathbf{C})&=\mathbf{B}(\mathbf{A}\cdot\mathbf{C})-\mathbf{C}(\mathbf{A}\cdot\mathbf{B}) ~~~~~\text{"bac-cab rule"} \\
\nabla\cdot(\mathbf{A}\times\mathbf{B}) &= (\nabla\times\mathbf{A})\cdot\mathbf{B}-(\nabla\times\mathbf{B})\cdot\mathbf{A} \\
\nabla\times(a\mathbf{A}) &= \nabla a\times\mathbf{A}+a\nabla\times\mathbf{A} \\
(\mathbf{A}\times\mathbf{B})\cdot(\mathbf{C}\times\mathbf{D}) &= (\mathbf{A}\cdot\mathbf{C})(\mathbf{B}\cdot\mathbf{D})-(\mathbf{A}\cdot\mathbf{D})(\mathbf{B}\cdot\mathbf{C}) \\
\nabla\cdot(a\mathbf{A}) &= \nabla a\cdot\mathbf{A}+a\nabla\cdot\mathbf{A} \\
\nabla \times \left(\nabla \times \mathbf{A} \right) &= \nabla \nabla \cdot
 \mathbf{A}-\Delta \mathbf{A} \\
\mathbf{A} \times \left( \nabla \times \mathbf{B} \right) &= \left( \nabla \mathbf{B}\right) \cdot \mathbf{A} - \mathbf{A} \cdot \nabla \mathbf{B} \\
\left( \mathbf{A} \times \nabla \right) \times \mathbf{B} &= \left( \nabla \mathbf{B}\right) \cdot \mathbf{A} - \mathbf{A}  \nabla \cdot \mathbf{B} \\
\nabla  \left( \mathbf{A}\cdot \mathbf{B} \right) &= \left( \nabla \mathbf{A} \right) \cdot \mathbf{B} +\left( \nabla \mathbf{B} \right) \cdot \mathbf{A} = \mathbf{A} \cdot \nabla \mathbf{B} + \mathbf{B} \cdot \nabla \mathbf{A} + \mathbf{A} \times \left( \nabla \times\mathbf{B} \right) + \mathbf{B} \times \left( \nabla \times\mathbf{A} \right)\\
\nabla \cdot \left( \mathbf{A} \mathbf{B} \right) &= \mathbf{A} \cdot \nabla \mathbf{B} + \mathbf{B} \nabla \cdot \mathbf{A} \\
\nabla \times\left( \mathbf{A} \times \mathbf{B} \right) &= \nabla \cdot \left( \mathbf{B}\mathbf{A}-\mathbf{A}\mathbf{B}\right) = \mathbf{A}\nabla \cdot\mathbf{B} + \mathbf{B} \cdot \nabla\mathbf{A} - \mathbf{B} \nabla \cdot \mathbf{A} - \mathbf{A} \cdot \nabla \mathbf{B}
\end{align}$$

Please add new vector identities at the end to keep the numbering unchanged!