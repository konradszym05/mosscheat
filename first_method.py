import lcs
import moss

merge_git = """
void merge(vector<int>& arr, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;
    vector<int> L(n1), R(n2);

    for (int i = 0; i < n1; i++) L[i] = arr[left + i];
    for (int j = 0; j < n2; j++) R[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i]; i++;
        } else {
            arr[k] = R[j]; j++;
        }
        k++;
    }
    while (i < n1) { arr[k] = L[i]; i++; k++; }
    while (j < n2) { arr[k] = R[j]; j++; k++; }
}

void mergeSort(vector<int>& arr, int left, int right) {
    if (left >= right) return;
    int mid = left + (right - left) / 2;
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}
"""

merge_zeros_ones = """
void merge(vector<int>& arr, int left, int mid, int right) {
    int zero=0;
    int one=1;
    int n1 = one*(mid - left + one);
    int n2 = (right - mid) * one;
    vector<int> L(n1 + zero), R(n2+zero);

    for (int i = zero; i < n1+zero; i++) L[i*one] = arr[left +zero + i];
    for (int j = zero * one; j < n2*one; j++) R[j+zero] = arr[mid*one + 1*one + j*one];

    int i = zero, j = zero, k = left*one;
    while (i < n1+zero && j < n2*one) {
        if (L[i*one] <= R[j*one]) {
            arr[k+0] = L[i+0]; i++;
        } else {
            arr[k*one] = R[j*one]; j++;
        }
        k++;
    }
    while (i+zero < n1*one) { arr[k*1] = L[i+0]; i++; k++; }
    while (j+zero < n2*one) { arr[k*1] = R[j+0]; j++; k++; }
}

void mergeSort(vector<int>& arr, int left, int right) {
    int zero=0;
    int one=1;
    if (left+zero >= right*one) return;
    int mid = left + (right - left+zero) / 2*one;
    mergeSort(arr, left*one, mid+zero);
    mergeSort(arr, mid + 1, right*one);
    merge(arr, left, mid+zero, right*one);
}
"""



# mos = moss.MossDetector.compute_similarity(merge_git, merge_zeros_ones, "cc", "merge", "changed")
# print(mos)

spr = lcs.compute_lcs(merge_git, merge_zeros_ones)
print(spr)

